from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class Article:
    title: str
    url: str
    source: str
    published: Optional[datetime] = None
    summary: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        d["published"] = self.published.isoformat() if self.published else None
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Article":
        pub = d.get("published")
        return cls(
            title=d["title"],
            url=d["url"],
            source=d["source"],
            published=datetime.fromisoformat(pub) if pub else None,
            summary=d.get("summary", ""),
        )
