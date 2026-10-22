from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, Sequence

from rich.console import Console
from rich.text import Text

from .models import Article


def _ago(dt: Optional[datetime]) -> str:
    if not dt:
        return ""
    secs = int((datetime.now(timezone.utc) - dt).total_seconds())
    if secs < 3600:
        return f"{max(secs // 60, 0)}m ago"
    if secs < 86400:
        return f"{secs // 3600}h ago"
    return f"{secs // 86400}d ago"


def render(articles: Sequence[Article], console: Optional[Console] = None, searched: bool = False) -> None:
    console = console or Console()
    if not articles:
        console.print("[yellow]No articles found.[/yellow]")
        if searched:
            console.print("Try another keyword, or remove -t to see everything.", style="dim")
        return
    for a in articles:
        head = Text()
        head.append(f"[{a.source}] ", style="bold cyan")
        head.append(a.title, style=f"bold link {a.url}")
        if a.published:
            head.append(f"  {_ago(a.published)}", style="dim")
        console.print(head)
        if a.summary:
            s = a.summary if len(a.summary) <= 160 else a.summary[:157] + "..."
            console.print(f"  {s}", style="dim", markup=False)
        console.print()
