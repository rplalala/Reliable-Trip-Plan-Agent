"""SSRF-resistant, bounded retrieval of one already observed HTML evidence URL."""

import asyncio
import codecs
import hashlib
import ipaddress
import re
import socket
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Protocol
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser

import httpx

from backend.app.integrations.web.page_models import (
    PageContentBlock,
    PageFetchRequest,
    PageFetchResult,
    PageFetchStatus,
)
from backend.app.runtime.config_models import PageRetrievalConfig

_REDIRECTS = {301, 302, 303, 307, 308}
_USER_AGENT = "ReliableTripPlanAgent/1.0"


@dataclass(frozen=True)
class RawPageResponse:
    status_code: int
    headers: dict[str, str]
    body: bytes


class PageHTTPTransport(Protocol):
    async def get(
        self, url: str, *, host: str, ip: str, max_bytes: int, timeout_seconds: float
    ) -> RawPageResponse: ...


class DomainResolver(Protocol):
    async def resolve(self, host: str) -> tuple[str, ...]: ...


class PublicDomainResolver:
    async def resolve(self, host: str) -> tuple[str, ...]:
        records = await asyncio.get_running_loop().getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        return tuple(sorted({record[4][0] for record in records}))


class HttpxPinnedPageTransport:
    """Connect to a checked IP while retaining the original Host and TLS SNI."""

    async def get(
        self, url: str, *, host: str, ip: str, max_bytes: int, timeout_seconds: float
    ) -> RawPageResponse:
        parts = urlsplit(url)
        ip_host = f"[{ip}]" if ":" in ip else ip
        pinned = urlunsplit(("https", ip_host, parts.path or "/", parts.query, ""))
        headers = {
            "Host": host,
            "User-Agent": _USER_AGENT,
            "Accept": "text/html",
            "Accept-Encoding": "identity",
        }
        async with httpx.AsyncClient(
            timeout=timeout_seconds, follow_redirects=False, trust_env=False
        ) as client:
            async with client.stream(
                "GET", pinned, headers=headers, extensions={"sni_hostname": host}
            ) as response:
                if response.status_code in _REDIRECTS:
                    return RawPageResponse(response.status_code, dict(response.headers), b"")
                declared = response.headers.get("content-length")
                if declared and declared.isdecimal() and int(declared) > max_bytes:
                    raise ValueError("Response body exceeds limit")
                body = bytearray()
                async for chunk in response.aiter_raw():
                    body.extend(chunk)
                    if len(body) > max_bytes:
                        raise ValueError("Response body exceeds limit")
                return RawPageResponse(response.status_code, dict(response.headers), bytes(body))


class _HTMLText(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript"}:
            self.skip_depth += 1
        if tag in {"p", "h1", "h2", "h3", "li", "br", "title"}:
            self.parts.append("\n")
        elif tag == "div":
            self.parts.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self.skip_depth:
            self.skip_depth -= 1
        if tag in {"p", "h1", "h2", "h3", "li", "title"}:
            self.parts.append("\n")
        elif tag == "div":
            self.parts.append(" ")

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.parts.append(data)


class _HTMLPageContext(HTMLParser):
    """Capture only fetched title and primary-body paragraph heading paths."""

    _VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta"}
    _EXCLUDED = {
        "nav",
        "aside",
        "footer",
        "header",
        "script",
        "style",
        "noscript",
        "iframe",
        "template",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.title: str | None = None
        self._title_parts: list[str] | None = None
        self._heading_tag: str | None = None
        self._heading_parts: list[str] = []
        self._headings: list[tuple[int, str]] = []
        self._block_tag: str | None = None
        self._block_parts: list[str] = []
        self.blocks: list[PageContentBlock] = []

    def _primary(self) -> bool:
        return "main" in self.stack and not any(tag in self.stack for tag in self._EXCLUDED)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in self._VOID_TAGS:
            self.stack.append(tag)
        if tag == "title" and "head" in self.stack and self.title is None:
            self._title_parts = []
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"} and self._primary():
            self._heading_tag = tag
            self._heading_parts = []
        elif tag in {"p", "li"} and self._primary() and self._block_tag is None:
            self._block_tag = tag
            self._block_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self._title_parts is not None:
            self.title = " ".join("".join(self._title_parts).split()) or None
            self._title_parts = None
        if tag == self._heading_tag:
            heading = " ".join("".join(self._heading_parts).split())
            if heading:
                level = int(tag[1])
                self._headings = [item for item in self._headings if item[0] < level]
                self._headings.append((level, heading))
            self._heading_tag = None
            self._heading_parts = []
        if tag == self._block_tag:
            body = " ".join("".join(self._block_parts).split())
            if body:
                self.blocks.append(
                    PageContentBlock(
                        text=body,
                        section_headings=tuple(item[1] for item in self._headings),
                    )
                )
            self._block_tag = None
            self._block_parts = []
        if tag in self.stack:
            index = len(self.stack) - 1 - self.stack[::-1].index(tag)
            del self.stack[index:]

    def handle_data(self, data: str) -> None:
        if self._title_parts is not None:
            self._title_parts.append(data)
        if self._heading_tag and self._primary():
            self._heading_parts.append(data)
        if self._block_tag and self._primary() and "a" not in self.stack:
            self._block_parts.append(data)


def _validated_host(url: str, allowed_domains: tuple[str, ...]) -> str:
    parts = urlsplit(url)
    if parts.scheme.casefold() != "https" or parts.username or parts.password:
        raise ValueError("Only credential-free HTTPS URLs are allowed")
    try:
        host = (parts.hostname or "").rstrip(".").encode("idna").decode("ascii").casefold()
        if parts.port not in (None, 443):
            raise ValueError("Only HTTPS port 443 is allowed")
    except (UnicodeError, ValueError) as exc:
        raise ValueError("Invalid HTTPS host or port") from exc
    if not host or host == "localhost" or host.endswith(".localhost"):
        raise ValueError("Localhost is not allowed")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        raise ValueError("IP-literal URLs are not allowed")
    if not any(host == domain or host.endswith(f".{domain}") for domain in allowed_domains):
        raise ValueError("URL is outside the task's authorized domains")
    return host


def _public_addresses(addresses: tuple[str, ...]) -> str:
    if not addresses:
        raise ValueError("DNS returned no addresses")
    parsed = [ipaddress.ip_address(address) for address in addresses]
    if not all(address.is_global for address in parsed):
        raise ValueError("DNS includes non-public or metadata addresses")
    return str(parsed[0])


def _html_text(
    response: RawPageResponse, max_chars: int
) -> tuple[str, str | None, tuple[PageContentBlock, ...]]:
    content_type = response.headers.get("content-type", "").casefold()
    if content_type.split(";", 1)[0].strip() != "text/html":
        raise TypeError("Only text/html is supported")
    encoding = response.headers.get("content-encoding", "identity").casefold().strip()
    if encoding not in ("", "identity") or response.body.startswith((b"\x1f\x8b", b"\x78\x9c")):
        raise TypeError("Compressed page content is unsupported")
    match = re.search(r"charset\s*=\s*['\"]?([a-zA-Z0-9._-]+)", content_type)
    charset = match.group(1) if match else "utf-8"
    try:
        codecs.lookup(charset)
        decoded = response.body.decode(charset, errors="strict")
    except (LookupError, UnicodeDecodeError) as exc:
        raise TypeError("HTML charset cannot be decoded safely") from exc
    parser = _HTMLText()
    parser.feed(decoded)
    context = _HTMLPageContext()
    context.feed(decoded)
    lines = (" ".join(line.split()) for line in "".join(parser.parts).splitlines())
    text = "\n".join(line for line in lines if line)[:max_chars]
    blocks = tuple(
        block for block in context.blocks if block.text[: min(40, len(block.text))] in text
    )
    return text, context.title if context.title and context.title in text else None, blocks


class SafeHTMLPageRetriever:
    """Retrieve only current-task observed URLs; robots is metadata, never evidence."""

    def __init__(
        self,
        config: PageRetrievalConfig,
        *,
        resolver: DomainResolver | None = None,
        transport: PageHTTPTransport | None = None,
    ) -> None:
        self._config = config
        self._resolver = resolver or PublicDomainResolver()
        self._transport = transport or HttpxPinnedPageTransport()
        self._robots: dict[str, RobotFileParser | bool] = {}

    async def fetch(self, request: PageFetchRequest) -> PageFetchResult:
        requests = 0
        chain: list[str] = []
        current = request.observed_url

        def result(
            status: PageFetchStatus, reason: str, *, final: str | None = None
        ) -> PageFetchResult:
            return PageFetchResult(
                task_id=request.task_id,
                observed_url=request.observed_url,
                status=status,
                final_url=final,
                redirect_chain=tuple(chain),
                http_request_count=requests,
                reason=reason,
            )

        if request.observed_url not in request.observed_urls:
            return result(PageFetchStatus.BLOCKED, "unobserved_target")
        try:
            async with asyncio.timeout(self._config.timeout_seconds):
                for redirect_count in range(self._config.max_redirects + 1):
                    host = _validated_host(current, request.allowed_domains)
                    ip = _public_addresses(await self._resolver.resolve(host))
                    origin = f"https://{host}"
                    if origin not in self._robots:
                        # robots.txt is the sole derived control-plane URL.
                        robots_url = origin + "/robots.txt"
                        requests += 1
                        policy = await self._transport.get(
                            robots_url,
                            host=host,
                            ip=ip,
                            max_bytes=self._config.max_response_bytes,
                            timeout_seconds=self._config.timeout_seconds,
                        )
                        if len(policy.body) > self._config.max_response_bytes:
                            return result(PageFetchStatus.OVERSIZED, "robots_oversized")
                        if policy.status_code in (404, 410):
                            self._robots[origin] = True
                        elif policy.status_code == 200:
                            if policy.headers.get(
                                "content-encoding", "identity"
                            ).casefold() not in (
                                "",
                                "identity",
                            ) or policy.body.startswith((b"\x1f\x8b", b"\x78\x9c")):
                                return result(PageFetchStatus.BLOCKED, "robots_compressed")
                            parser = RobotFileParser()
                            parser.parse(policy.body.decode("utf-8", errors="replace").splitlines())
                            self._robots[origin] = parser
                        else:
                            return result(PageFetchStatus.BLOCKED, "robots_unavailable")
                    robots = self._robots[origin]
                    if isinstance(robots, RobotFileParser) and not robots.can_fetch(
                        _USER_AGENT, current
                    ):
                        return result(PageFetchStatus.BLOCKED, "robots_disallow")
                    requests += 1
                    response = await self._transport.get(
                        current,
                        host=host,
                        ip=ip,
                        max_bytes=self._config.max_response_bytes,
                        timeout_seconds=self._config.timeout_seconds,
                    )
                    if len(response.body) > self._config.max_response_bytes:
                        return result(PageFetchStatus.OVERSIZED, "page_oversized", final=current)
                    if response.status_code in _REDIRECTS:
                        location = response.headers.get("location")
                        if not location or redirect_count >= self._config.max_redirects:
                            return result(PageFetchStatus.BLOCKED, "redirect_limit", final=current)
                        chain.append(current)
                        current = urljoin(current, location)
                        continue
                    if response.status_code != 200:
                        return result(PageFetchStatus.INACCESSIBLE, "http_status", final=current)
                    try:
                        text, page_title, content_blocks = _html_text(
                            response, self._config.max_text_chars
                        )
                    except TypeError:
                        return result(
                            PageFetchStatus.UNSUPPORTED, "unsupported_content", final=current
                        )
                    if not text:
                        return result(PageFetchStatus.UNSUPPORTED, "empty_html_text", final=current)
                    return PageFetchResult(
                        task_id=request.task_id,
                        observed_url=request.observed_url,
                        status=PageFetchStatus.FETCHED,
                        final_url=current,
                        redirect_chain=tuple(chain),
                        authorized_domain=host,
                        text=text,
                        page_title=page_title,
                        content_blocks=content_blocks,
                        body_sha256=hashlib.sha256(response.body).hexdigest(),
                        http_request_count=requests,
                    )
        except TimeoutError:
            return result(PageFetchStatus.TIMEOUT, "timeout", final=current)
        except ValueError as exc:
            reason = "oversized" if "exceeds limit" in str(exc) else "unsafe_url_or_dns"
            status = PageFetchStatus.OVERSIZED if reason == "oversized" else PageFetchStatus.BLOCKED
            return result(status, reason, final=current)
        except (OSError, httpx.HTTPError):
            return result(PageFetchStatus.INACCESSIBLE, "network_error", final=current)
        return result(PageFetchStatus.BLOCKED, "redirect_limit", final=current)
