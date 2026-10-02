"""Prepare, deliver and replay local blinded ranking artifacts without network calls."""

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path

from .human_answers import validate_answers
from .human_report import build_human_report
from .human_tasks import build_human_package, prepare_human_material
from .intake import _read
from .records import MaterialError, require


def render_human_html(public, javascript, css):
    """Embed only anonymous JSON and the trusted isolated offline renderer assets."""
    require(
        isinstance(javascript, str) and javascript.strip() and isinstance(css, str),
        "renderer",
        "Renderer JavaScript and CSS required",
    )
    require(
        not re.search(r"sourceMappingURL|\bimport\s*\(|\bfetch\s*\(|</script", javascript, re.I)
        and not re.search(r"@import|url\s*\(|</style", css, re.I),
        "renderer",
        "Renderer must have no external dependencies, script terminator or source maps",
    )
    data = json.dumps(public, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    for char, escaped in (
        ("<", "\\u003c"),
        ("&", "\\u0026"),
        ("\u2028", "\\u2028"),
        ("\u2029", "\\u2029"),
    ):
        data = data.replace(char, escaped)
    policy = (
        "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; "
        "connect-src 'none'; base-uri 'none'; form-action 'none'"
    )
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<meta http-equiv="Content-Security-Policy" content="{policy}">'
        f"<title>Travel plan review</title><style>{css}</style></head><body>"
        '<div id="root"></div><noscript>JavaScript is required for local ranking '
        'and JSON backup.</noscript>'
        f'<script id="human-data" type="application/json">{data}</script>'
        f'<script>{javascript}</script></body></html>'
    )


def _write(path, content):
    target = Path(path)
    require(not target.exists(), "output", "Output exists; use a new artifact path")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(content)


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("prepare", "package"):
        command = commands.add_parser(name)
        command.add_argument("manifest")
        command.add_argument("config")
        if name == "package":
            command.add_argument("review")
            command.add_argument("--private-out", required=True)
            command.add_argument("--renderer-js", required=True)
            command.add_argument("--renderer-css", required=True)
        command.add_argument("--out", required=name == "package")
    for name in ("import", "report"):
        command = commands.add_parser(name)
        command.add_argument("presentation")
        command.add_argument("mapping")
        command.add_argument("answers", nargs="*")
        command.add_argument("--out")
        if name == "report":
            command.add_argument("--generated-at")
    args = parser.parse_args(argv)
    try:
        if args.command in ("prepare", "package"):
            config, _ = _read(Path(args.config))
            if args.command == "prepare":
                result = prepare_human_material(args.manifest, config)
            else:
                review, _ = _read(Path(args.review))
                package = build_human_package(args.manifest, config, review)
                directory = Path(args.out).resolve()
                private = Path(args.private_out).resolve()
                require(
                    not private.is_relative_to(directory),
                    "private-out",
                    "Private mapping must stay outside public directory",
                )
                require(
                    not directory.exists() and not private.exists(),
                    "output",
                    "Package outputs must be new paths",
                )
                html = render_human_html(
                    package["public"],
                    Path(args.renderer_js).read_text(encoding="utf-8"),
                    Path(args.renderer_css).read_text(encoding="utf-8"),
                )
                _write(private, _json(package["private"]))
                _write(directory / "presentation.json", _json(package["public"]))
                _write(directory / "review.html", html)
                print(
                    _json(
                        {"status": "complete", "public_files": ["review.html", "presentation.json"]}
                    )
                )
                return 0
        else:
            public, _ = _read(Path(args.presentation))
            private, _ = _read(Path(args.mapping))
            bundles = [_read(Path(p))[0] for p in args.answers]
            result = (
                validate_answers(public, private, bundles)
                if args.command == "import"
                else build_human_report(
                    public,
                    private,
                    bundles,
                    generated_at=args.generated_at or datetime.now(UTC).isoformat(),
                )
            )
        if args.out:
            _write(args.out, _json(result))
        else:
            print(_json(result))
        return 0
    except (MaterialError, OSError, ValueError, TypeError, KeyError) as exc:
        diagnostic = (
            exc.diagnostic
            if isinstance(exc, MaterialError)
            else {
                "reason": "artifact_integrity_error",
                "pointer": "human_cli",
                "explanation": str(exc),
            }
        )
        print(_json({"status": "needs_material_correction", "diagnostics": [diagnostic]}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
