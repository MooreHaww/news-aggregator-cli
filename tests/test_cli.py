from typer.testing import CliRunner

from newsfeed import cli
from newsfeed.models import Article

TIP = "Tip: filter by topic with newsfeed fetch -t football"


def _art(title="Football news"):
    return Article(source="bbc", title=title, url="https://x/" + title, summary="", published=None)


def _run(monkeypatch, args, articles):
    monkeypatch.setattr(cli, "DEFAULT_SOURCES", {"bbc": "u"})
    monkeypatch.setattr(cli, "_get", lambda name, refresh: articles)
    try:
        runner = CliRunner(mix_stderr=False)
    except TypeError:  # click >= 8.2 always separates stderr
        runner = CliRunner()
    return runner.invoke(cli.app, args)


def test_no_command_prints_welcome():
    result = CliRunner().invoke(cli.app, [])
    assert result.exit_code == 0
    for line in ("newsfeed sources", "newsfeed fetch -n 5", "newsfeed fetch -t football -n 5"):
        assert line in result.output
    assert "keyword you type yourself" in result.output


def test_tip_on_stderr_without_topic(monkeypatch):
    result = _run(monkeypatch, ["fetch"], [_art()])
    assert TIP in result.stderr
    assert TIP not in result.stdout


def test_no_tip_with_topic(monkeypatch):
    result = _run(monkeypatch, ["fetch", "-t", "football"], [_art()])
    assert TIP not in result.stderr
    assert TIP not in result.stdout


def test_no_articles_with_topic_suggests_alternatives(monkeypatch):
    result = _run(monkeypatch, ["fetch", "-t", "zzzz"], [_art()])
    assert "No articles found." in result.stdout
    assert "another keyword" in result.stdout
    assert "remove -t" in result.stdout
    assert TIP not in result.stderr


def test_no_articles_without_topic_has_no_suggestion(monkeypatch):
    result = _run(monkeypatch, ["fetch"], [])
    assert "No articles found." in result.stdout
    assert "another keyword" not in result.stdout
