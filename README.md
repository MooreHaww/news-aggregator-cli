# newsfeed

Pull headlines from several RSS feeds (BBC, NYT, Guardian, Hacker News), dedupe, cache and filter them, and print a clean feed in your terminal. No API keys.

![newsfeed demo](docs/demo.png)

```
pip install .
newsfeed sources
newsfeed fetch -t ai -t climate -n 10
newsfeed fetch -s bbc -s hn --refresh
```

Results are cached for 15 minutes; `--refresh` bypasses the cache.

## Performance

A fresh fetch of all four feeds takes about 1.162927 seconds. A cached fetch takes about 0.2842921 seconds, roughly 4x faster.

## Development
```
pip install -e ".[dev]"
pytest
```
