import time
from datetime import datetime, timezone

from newsfeed import cache
from newsfeed.dedupe import dedupe
from newsfeed.fetcher import parse_feed
from newsfeed.filters import filter_topics, limit, sort_newest
from newsfeed.models import Article

RSS = b"""<?xml version="1.0"?><rss version="2.0"><channel><title>t</title>
<item><title>AI boom</title><link>http://x.com/a</link>
<description>&lt;p&gt;About chips&lt;/p&gt;</description>
<pubDate>Mon, 01 Jan 2024 10:00:00 GMT</pubDate></item>
<item><title></title><link>http://x.com/b</link></item></channel></rss>"""


def A(title, url, pub=None, summary=""):
    return Article(title, url, "s", pub, summary)


def test_parse_feed():
    arts = parse_feed(RSS, "src")
    assert len(arts) == 1
    assert arts[0].source == "src" and arts[0].published.year == 2024
    assert arts[0].summary == "About chips"


def test_dedupe_by_url_and_title():
    out = dedupe([A("Hello World", "https://www.a.com/x/?u=1"), A("Other", "http://a.com/x"),
                  A("hello, world!", "http://b.com/y"), A("New", "http://c.com/z")])
    assert [a.title for a in out] == ["Hello World", "New"]


def test_filter_sort_limit():
    old = datetime(2020, 1, 1, tzinfo=timezone.utc)
    new = datetime(2024, 1, 1, tzinfo=timezone.utc)
    arts = [A("Old AI", "u1", old), A("Cats", "u2", new, "ai inside"), A("Dogs", "u3", new)]
    f = filter_topics(arts, ["AI"])
    assert [a.url for a in sort_newest(f)] == ["u2", "u1"]
    assert len(limit(arts, 1)) == 1


def test_cache_ttl(tmp_path):
    arts = [A("T", "u", datetime(2024, 1, 1, tzinfo=timezone.utc))]
    cache.save("s", arts, tmp_path)
    assert cache.load("s", 60, tmp_path)[0].title == "T"
    time.sleep(0.01)
    assert cache.load("s", 0, tmp_path) is None
    assert cache.load("missing", 60, tmp_path) is None
