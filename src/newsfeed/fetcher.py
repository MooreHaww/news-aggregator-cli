from __future__ import annotations

import re
from calendar import timegm
from datetime import datetime, timezone
from typing import List

import feedparser
import requests

from .models import Article

HEADERS = {"User-Agent": "newsfeed-cli/0.1 (+RSS reader)"}
_TAG_RE = re.compile(r"<[^>]+>")


_HN_ARTICLE_RE = re.compile(r"Article URL:\s*(\S+)")
_HN_POINTS_RE = re.compile(r"Points:\s*(\d+)")
_HN_COMMENTS_RE = re.compile(r"#\s*Comments:\s*(\d+)")


def _plural(n: int, word: str) -> str:
    return f"{n} {word}" + ("" if n == 1 else "s")


def _clean_hn(summary: str, url: str):
    """Turn hnrss's raw summary into '296 points · 240 comments' and the article URL."""
    article = _HN_ARTICLE_RE.search(summary)
    points = _HN_POINTS_RE.search(summary)
    comments = _HN_COMMENTS_RE.search(summary)
    if not (article or points or comments):
        return summary, url
    parts = []
    if points:
        parts.append(_plural(int(points.group(1)), "point"))
    if comments:
        parts.append(_plural(int(comments.group(1)), "comment"))
    return " · ".join(parts), (article.group(1) if article else url)


def parse_feed(content: bytes, source: str) -> List[Article]:
    parsed = feedparser.parse(content)
    articles = []
    for e in parsed.entries:
        title = _TAG_RE.sub("", e.get("title") or "").strip()
        url = e.get("link") or ""
        if not title or not url:
            continue
        ts = e.get("published_parsed") or e.get("updated_parsed")
        published = datetime.fromtimestamp(timegm(ts), tz=timezone.utc) if ts else None
        summary = _TAG_RE.sub("", e.get("summary", "")).strip()
        summary, url = _clean_hn(summary, url)
        articles.append(Article(title, url, source, published, summary))
    return articles


def fetch_feed(source: str, url: str, timeout: float = 10) -> List[Article]:
    resp = requests.get(url, headers=HEADERS, timeout=timeout)
    resp.raise_for_status()
    return parse_feed(resp.content, source)
