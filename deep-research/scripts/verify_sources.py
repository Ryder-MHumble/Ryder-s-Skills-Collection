#!/usr/bin/env python3
"""Verify source URLs and simple keyword hits for evidence-led reports.

Input CSV columns:
  url,keywords[,claim]

keywords are semicolon-separated. Output CSV adds HTTP status, page title,
keyword hit counts, and a mechanical verdict. This script is a pre-screen only;
final claim support still requires human/agent judgment.
"""

from __future__ import annotations

import argparse
import csv
import html
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


class TitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._in_title = False
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[override]
        if tag.lower() == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:  # type: ignore[override]
        if tag.lower() == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:  # type: ignore[override]
        if self._in_title:
            self.parts.append(data)

    @property
    def title(self) -> str:
        return " ".join(part.strip() for part in self.parts if part.strip())


def normalize_text(value: str) -> str:
    value = html.unescape(value)
    value = re.sub(r"<script\b.*?</script>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<style\b.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def fetch(url: str, timeout: int) -> tuple[int | str, str, str]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; deep-research-report/1.0)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec - user-provided research URLs
            status = getattr(resp, "status", resp.getcode())
            raw = resp.read(1_500_000)
            encoding = resp.headers.get_content_charset() or "utf-8"
            text = raw.decode(encoding, errors="replace")
    except urllib.error.HTTPError as exc:
        try:
            raw = exc.read(200_000)
            text = raw.decode("utf-8", errors="replace")
        except Exception:
            text = ""
        return exc.code, "", normalize_text(text)[:5000]
    except Exception as exc:  # network, DNS, TLS, timeout
        return "ERR", "", f"{type(exc).__name__}: {exc}"

    parser = TitleParser()
    try:
        parser.feed(text)
    except Exception:
        pass
    return status, parser.title, normalize_text(text)


def keyword_hits(body: str, keywords: str) -> tuple[int, str]:
    terms = [term.strip() for term in re.split(r"[;；]", keywords or "") if term.strip()]
    if not terms:
        return 0, ""
    low = body.lower()
    hits = [term for term in terms if term.lower() in low]
    return len(hits), ";".join(hits)


def verdict(status: int | str, hits: int, total_keywords: int) -> str:
    if status in (200, 301, 302):
        if total_keywords == 0:
            return "reachable_no_keywords"
        if hits > 0:
            return "reachable_keyword_hit"
        return "reachable_no_keyword_hit"
    if status == 403:
        return "browser_required_or_blocked"
    return "unreachable"


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify source URLs and keyword hits.")
    parser.add_argument("input", help="CSV with url,keywords[,claim]")
    parser.add_argument("--timeout", type=int, default=12)
    parser.add_argument("--out", help="Output CSV path. Defaults to stdout.")
    args = parser.parse_args()

    input_path = Path(args.input)
    rows = list(csv.DictReader(input_path.open(newline="", encoding="utf-8-sig")))
    fieldnames = list(rows[0].keys()) if rows else ["url", "keywords"]
    extra = ["http_status", "title", "keyword_hits", "matched_keywords", "verdict"]
    output_rows = []

    for row in rows:
        url = (row.get("url") or "").strip()
        keywords = row.get("keywords") or ""
        if not url:
            status, title, body = "ERR", "", "missing url"
        else:
            status, title, body = fetch(url, args.timeout)
        hits, matched = keyword_hits(" ".join([title, body]), keywords)
        total = len([term for term in re.split(r"[;；]", keywords) if term.strip()])
        row.update(
            {
                "http_status": status,
                "title": title,
                "keyword_hits": hits,
                "matched_keywords": matched,
                "verdict": verdict(status, hits, total),
            }
        )
        output_rows.append(row)

    out = open(args.out, "w", newline="", encoding="utf-8") if args.out else sys.stdout
    try:
        writer = csv.DictWriter(out, fieldnames=fieldnames + [f for f in extra if f not in fieldnames])
        writer.writeheader()
        writer.writerows(output_rows)
    finally:
        if args.out:
            out.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
