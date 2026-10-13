from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional, Sequence

from .models import Article

_MIN = datetime.min.replace(tzinfo=timezone.utc)


def filter_topics(articles: Sequence[Article], topics: Sequence[str]) -> List[Article]:
    if not topics:
        return list(articles)
    terms = [t.lower() for t in topics]
    return [a for a in articles if any(t in f"{a.title} {a.summary}".lower() for t in terms)]


def sort_newest(articles: Sequence[Article]) -> List[Article]:
    return sorted(articles, key=lambda a: a.published or _MIN, reverse=True)


def limit(articles: Sequence[Article], n: Optional[int]) -> List[Article]:
    return list(articles[:n]) if n else list(articles)
