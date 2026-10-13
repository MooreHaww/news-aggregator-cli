from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional

import typer
from rich.console import Console

from . import __version__, cache
from .dedupe import dedupe
from .fetcher import fetch_feed
from .filters import filter_topics, limit as limit_articles, sort_newest
from .render import render
from .sources import DEFAULT_SOURCES

app = typer.Typer(help="Aggregate headlines from RSS feeds.", add_completion=False)
err = Console(stderr=True)


def _version(value: bool):
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def main(version: bool = typer.Option(False, "--version", callback=_version, is_eager=True)):
    pass


def _get(name: str, refresh: bool):
    if not refresh:
        cached = cache.load(name)
        if cached is not None:
            return cached
    try:
        articles = fetch_feed(name, DEFAULT_SOURCES[name])
    except Exception as e:
        err.print(f"[red]warning:[/red] {name} failed: {e}")
        return []
    cache.save(name, articles)
    return articles


@app.command()
def fetch(
    topic: Optional[List[str]] = typer.Option(None, "--topic", "-t", help="Keyword filter (repeatable)."),
    source: Optional[List[str]] = typer.Option(None, "--source", "-s", help="Source name (repeatable)."),
    limit: int = typer.Option(20, "--limit", "-n"),
    refresh: bool = typer.Option(False, "--refresh", help="Ignore the cache."),
):
    """Fetch, dedupe, filter and print headlines."""
    names = source or list(DEFAULT_SOURCES)
    unknown = [n for n in names if n not in DEFAULT_SOURCES]
    if unknown:
        err.print(f"[red]Unknown source(s):[/red] {', '.join(unknown)}")
        raise typer.Exit(2)
    with ThreadPoolExecutor(max_workers=len(names)) as pool:
        results = list(pool.map(lambda n: _get(n, refresh), names))
    articles = [a for batch in results for a in batch]
    articles = dedupe(sort_newest(articles))
    articles = limit_articles(filter_topics(articles, topic or []), limit)
    render(articles)


@app.command()
def sources():
    """List available sources."""
    for name, url in DEFAULT_SOURCES.items():
        typer.echo(f"{name:10} {url}")
