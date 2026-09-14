"""Offline PageRetriever checks for observed-target, access, and SSRF bounds."""

import asyncio

from backend.app.integrations.web.http_page_retriever import (
    RawPageResponse,
    SafeHTMLPageRetriever,
)
from backend.app.integrations.web.page_models import PageFetchRequest, PageFetchStatus
from backend.app.runtime.config_loader import load_runtime_config

URL = "https://alpha.example.org/notice"
ROBOTS = "https://alpha.example.org/robots.txt"


class FakeResolver:
    def __init__(self, addresses=("8.8.8.8",)):
        self.addresses = addresses
        self.calls = []

    async def resolve(self, host):
        self.calls.append(host)
        return self.addresses


class FakeTransport:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    async def get(self, url, *, host, ip, max_bytes, timeout_seconds):
        self.calls.append((url, host, ip, max_bytes, timeout_seconds))
        return self.responses[url]


def _request(url=URL, observed_urls=(URL,), domains=("alpha.example.org",)):
    return PageFetchRequest(
        task_id="task-1",
        observed_url=url,
        observed_urls=observed_urls,
        allowed_domains=domains,
    )


def _run(responses, request=None, *, resolver=None):
    transport = FakeTransport(responses)
    retriever = SafeHTMLPageRetriever(
        load_runtime_config().web_evidence.page_retrieval,
        resolver=resolver or FakeResolver(),
        transport=transport,
    )
    result = asyncio.run(retriever.fetch(request or _request()))
    return result, transport


def test_fetches_observed_html_with_pinned_public_ip_and_robots_control_request() -> None:
    result, transport = _run(
        {
            ROBOTS: RawPageResponse(404, {}, b""),
            URL: RawPageResponse(
                200,
                {"content-type": "text/html"},
                b"<html><h1>Alpha Zoo</h1><script>ignore me</script><p>Closed today</p></html>",
            ),
        }
    )
    assert result.status is PageFetchStatus.FETCHED
    assert result.text == "Alpha Zoo\nClosed today"
    assert result.final_url == URL
    assert result.body_sha256
    assert result.http_request_count == 2
    assert [item[0] for item in transport.calls] == [ROBOTS, URL]
    assert all(item[2] == "8.8.8.8" for item in transport.calls)


def test_page_context_records_title_and_primary_section_but_excludes_related_content() -> None:
    html = (
        "<html><head><title>Admission - Alpha Zoo</title></head><body>"
        "<nav><p>Beta Zoo tickets are required.</p></nav>"
        "<main><h1>Admission</h1><h2>Tickets</h2>"
        "<p>Tickets are not required for permanent exhibitions.</p>"
        "<aside><p>Beta Zoo tickets are required.</p></aside>"
        "<p><a href='/other'>Beta Zoo tickets are required.</a></p>"
        "<svg><title>Beta Zoo</title></svg>"
        "</main></body></html>"
    )
    result, _ = _run(
        {
            ROBOTS: RawPageResponse(404, {}, b""),
            URL: RawPageResponse(200, {"content-type": "text/html"}, html.encode()),
        }
    )
    assert result.status is PageFetchStatus.FETCHED
    assert result.page_title == "Admission - Alpha Zoo"
    assert len(result.content_blocks) == 1
    assert result.content_blocks[0].text == ("Tickets are not required for permanent exhibitions.")
    assert result.content_blocks[0].section_headings == ("Admission", "Tickets")


def test_unobserved_url_never_causes_http_or_dns_activity() -> None:
    resolver = FakeResolver()
    result, transport = _run({}, _request("https://alpha.example.org/invented"), resolver=resolver)
    assert result.status is PageFetchStatus.BLOCKED
    assert result.reason == "unobserved_target"
    assert result.http_request_count == 0
    assert resolver.calls == transport.calls == []


def test_private_or_metadata_dns_answer_is_rejected_before_http() -> None:
    for addresses in (("169.254.169.254",), ("8.8.8.8", "127.0.0.1")):
        result, transport = _run({}, resolver=FakeResolver(addresses))
        assert result.status is PageFetchStatus.BLOCKED
        assert result.http_request_count == 0
        assert transport.calls == []


def test_robots_disallow_blocks_content_fetch() -> None:
    result, transport = _run(
        {ROBOTS: RawPageResponse(200, {}, b"User-agent: *\nDisallow: /notice\n")}
    )
    assert result.status is PageFetchStatus.BLOCKED
    assert result.reason == "robots_disallow"
    assert [item[0] for item in transport.calls] == [ROBOTS]


def test_redirect_is_rechecked_and_unauthorized_target_is_never_fetched() -> None:
    result, transport = _run(
        {
            ROBOTS: RawPageResponse(404, {}, b""),
            URL: RawPageResponse(302, {"location": "https://outside.example.net/notice"}, b""),
        }
    )
    assert result.status is PageFetchStatus.BLOCKED
    assert result.reason == "unsafe_url_or_dns"
    assert result.redirect_chain == (URL,)
    assert [item[0] for item in transport.calls] == [ROBOTS, URL]


def test_allowed_redirect_stays_inside_one_bounded_target_attempt() -> None:
    final = "https://alpha.example.org/final"
    result, transport = _run(
        {
            ROBOTS: RawPageResponse(404, {}, b""),
            URL: RawPageResponse(302, {"location": "/final"}, b""),
            final: RawPageResponse(200, {"content-type": "text/html"}, b"<p>Alpha Zoo closed</p>"),
        }
    )
    assert result.status is PageFetchStatus.FETCHED
    assert result.redirect_chain == (URL,)
    assert result.final_url == final
    assert result.http_request_count == 3
    assert [item[0] for item in transport.calls] == [ROBOTS, URL, final]


def test_third_redirect_is_blocked_without_following_another_page() -> None:
    second = "https://alpha.example.org/second"
    third = "https://alpha.example.org/third"
    fourth = "https://alpha.example.org/fourth"
    result, transport = _run(
        {
            ROBOTS: RawPageResponse(404, {}, b""),
            URL: RawPageResponse(302, {"location": "/second"}, b""),
            second: RawPageResponse(302, {"location": "/third"}, b""),
            third: RawPageResponse(302, {"location": "/fourth"}, b""),
        }
    )
    assert result.status is PageFetchStatus.BLOCKED
    assert result.reason == "redirect_limit"
    assert result.http_request_count == 4
    assert [item[0] for item in transport.calls] == [ROBOTS, URL, second, third]
    assert fourth not in [item[0] for item in transport.calls]


def test_non_html_compressed_and_oversized_bodies_fail_boundedly() -> None:
    cases = (
        (
            RawPageResponse(200, {"content-type": "application/pdf"}, b"pdf"),
            PageFetchStatus.UNSUPPORTED,
        ),
        (
            RawPageResponse(200, {"content-type": "text/html", "content-encoding": "gzip"}, b"gz"),
            PageFetchStatus.UNSUPPORTED,
        ),
        (
            RawPageResponse(200, {"content-type": "text/html"}, b"x" * 262145),
            PageFetchStatus.OVERSIZED,
        ),
    )
    for page, expected in cases:
        result, _ = _run({ROBOTS: RawPageResponse(404, {}, b""), URL: page})
        assert result.status is expected
        assert result.http_request_count == 2
