from __future__ import annotations

import re
from typing import Iterable, List
from urllib.parse import urlsplit

from .models import Article


def _norm_url(url: str) -> str:
    p = urlsplit(url)
    host = p.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return f"{host}{p.path.rstrip('/')}"


def _norm_title(title: str) -> str:
    return re.sub(r"\W+", " ", title.lower()).strip()


def dedupe(articles: Iterable[Article]) -> List[Article]:
    seen_urls, seen_titles, out = set(), set(), []
    for a in articles:
        u, t = _norm_url(a.url), _norm_title(a.title)
        if u in seen_urls or t in seen_titles:
            continue
        seen_urls.add(u)
        seen_titles.add(t)
        out.append(a)
    return out
