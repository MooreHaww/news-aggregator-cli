# newsfeed

Pull headlines from several RSS feeds (BBC, NYT, Guardian, Hacker News), dedupe, cache and filter them, and print a clean feed in your terminal. No API keys.

```
pip install .
newsfeed sources
newsfeed fetch -t ai -t climate -n 10
newsfeed fetch -s bbc -s hn --refresh
```

Results are cached for 15 minutes; `--refresh` bypasses the cache.

## Development
```
pip install -e ".[dev]"
pytest
```
