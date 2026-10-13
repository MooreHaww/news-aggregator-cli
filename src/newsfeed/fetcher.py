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
        articles.append(Article(title, url, source, published, summary))
    return articles


def fetch_feed(source: str, url: str, timeout: float = 10) -> List[Article]:
    resp = requests.get(url, headers=HEADERS, timeout=timeout)
    resp.raise_for_status()
    return parse_feed(resp.content, source)
