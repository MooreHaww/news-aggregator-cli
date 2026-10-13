from __future__ import annotations

import json
import time
from pathlib import Path
from typing import List, Optional

from platformdirs import user_cache_dir

from .models import Article

DEFAULT_TTL = 15 * 60


def cache_dir() -> Path:
    p = Path(user_cache_dir("newsfeed"))
    p.mkdir(parents=True, exist_ok=True)
    return p


def load(source: str, ttl: int = DEFAULT_TTL, directory: Optional[Path] = None) -> Optional[List[Article]]:
    path = (directory or cache_dir()) / f"{source}.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if time.time() - data["fetched_at"] > ttl:
            return None
        return [Article.from_dict(a) for a in data["articles"]]
    except (OSError, ValueError, KeyError):
        return None


def save(source: str, articles: List[Article], directory: Optional[Path] = None) -> None:
    path = (directory or cache_dir()) / f"{source}.json"
    payload = {"fetched_at": time.time(), "articles": [a.to_dict() for a in articles]}
    path.write_text(json.dumps(payload), encoding="utf-8")
