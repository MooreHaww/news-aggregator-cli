<div align="center">

# 📰 newsfeed

**Every headline you care about, in one clean terminal feed. No API keys, no tabs, no scrolling through five sites.**

![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MIT License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Release](https://img.shields.io/github/v/release/MooreHaww/news-aggregator-cli?style=for-the-badge&color=orange)
![No API keys](https://img.shields.io/badge/API%20keys-none-success?style=for-the-badge)
![Built with](https://img.shields.io/badge/built%20with-Typer%20%7C%20Rich-8A2BE2?style=for-the-badge)

![newsfeed demo](docs/demo.png)

</div>

---

## 💡 Why this project exists

Checking many news sites for the same topic takes time. `newsfeed` fetches BBC, NYT, The Guardian and Hacker News in one go, removes duplicates, and shows a single list you can filter by topic.

It is **project #1** of my build plan: a small tool I could finish in a week, to practise RSS handling, caching, testing and packaging, and to get a first complete repo onto GitHub.

## 🔎 What it does

- 📡 **Multiple sources:** BBC, NYT, The Guardian and Hacker News
- 🧹 **Duplicate removal:** the same story from two sources shows once (same URL or same title)
- ⚡ **15-minute cache:** repeat runs are about 4× faster
- 🎯 **Topic filter:** whole-word, case-insensitive matching
- 🎨 **Clean Rich output:** clickable titles, source labels, "published X ago", and points and comments for Hacker News
- 🔑 **No API keys**

Newest headlines come first. Flags combine freely: `newsfeed fetch -s guardian -t ai -n 10 --refresh`.

| Command / flag | What it does | Example |
| --- | --- | --- |
| `newsfeed fetch` | Fetch all sources and print the latest 20 headlines | `newsfeed fetch` |
| `-t`, `--topic TEXT` | Keep items whose title or summary contains this whole word. Repeat for any-of | `newsfeed fetch -t climate -t energy` |
| `-s`, `--source NAME` | Use only `bbc`, `nyt`, `guardian` or `hn`. Unknown names exit with code 2 | `newsfeed fetch -s bbc -s hn` |
| `-n`, `--limit N` | Maximum items to show (default 20) | `newsfeed fetch -n 5` |
| `--refresh` | Ignore the cache and download again | `newsfeed fetch --refresh` |
| `newsfeed sources` | List source names and feed URLs | `newsfeed sources` |
| `--version` | Print the installed version | `newsfeed --version` |

If nothing matches it prints `No articles found.` If one feed is unreachable, a warning is shown and the other sources still print.

**Measured:** a fresh fetch of all four feeds takes about **1.2 s**; a cached fetch about **0.3 s**.

## ⚙️ Setup

Requires Python 3.9 or newer. Check yours with:

```bash
python --version
```

(On Mac / Linux you may need `python3 --version`. If it is older than 3.9 or not found, install Python from [python.org](https://www.python.org/downloads/) first.)

There are two ways to get the code: **Clone** copies the project with its full history and needs Git, while **Download ZIP** gives you just the files and needs no Git. Both lead to the same next steps.

**Directly from GitHub** (needs Git)

```bash
pip install git+https://github.com/MooreHaww/news-aggregator-cli.git
```

**From a clone (Windows PowerShell)**

```powershell
git clone https://github.com/MooreHaww/news-aggregator-cli.git
cd news-aggregator-cli
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install .
```

**From a clone (Mac / Linux)**

```bash
git clone https://github.com/MooreHaww/news-aggregator-cli.git
cd news-aggregator-cli
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

**No Git? Download ZIP instead.** On the GitHub page click the green **Code** button, then **Download ZIP**, unzip it, and open a terminal inside the unzipped folder (it may be called `news-aggregator-cli-main`). Then run the same commands as above, starting from the `python -m venv .venv` line (`python3 -m venv .venv` on Mac / Linux).

Check it worked: `newsfeed --version`, then run `newsfeed fetch`.

## ▶️ Running it

Every time you open a **new terminal**, go into the project folder and activate the venv again, otherwise the `newsfeed` command won't be found.

**Windows (PowerShell)**

```powershell
cd path\to\news-aggregator-cli
.venv\Scripts\Activate.ps1
newsfeed fetch
```

**Mac / Linux**

```bash
cd path/to/news-aggregator-cli
source .venv/bin/activate
newsfeed fetch
```

`(.venv)` at the start of your prompt means the venv is active.

## 🚀 Your first run

```bash
newsfeed sources
newsfeed fetch -n 5
newsfeed fetch -t football -n 5
```

1. `newsfeed sources` lists the available sources.
2. `newsfeed fetch -n 5` shows the 5 newest headlines from all sources.
3. `newsfeed fetch -t football -n 5` shows the 5 newest headlines that mention "football".

`-t` is optional. It is a keyword you type yourself: swap `football` for any word, such as `climate` or `ai`. Leave it out to see everything.

## 🛠️ Troubleshooting

- **`newsfeed is not recognized` (or `command not found`):** the venv isn't activated in this terminal. Go into the project folder and run `.venv\Scripts\Activate.ps1` (Windows) or `source .venv/bin/activate` (Mac / Linux).
- **PowerShell blocks the activate script:** allow local scripts for your user once, then activate again:

  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
  ```

- **`make` / Makefile:** this project has none. Use the `pip` and `newsfeed` commands shown above.

**Run the tests** (they run offline):

```bash
pip install -e ".[dev]"
pytest
```

**Add your own source:** edit `src/newsfeed/sources.py`, add a name and an RSS or Atom URL, then use `newsfeed fetch -s <name>`:

```python
DEFAULT_SOURCES = {
    ...
    "verge": "https://www.theverge.com/rss/index.xml",
}
```

(Reinstall with `pip install .` unless you installed with `-e`.)

## 🎯 What I wanted to learn

- How RSS feeds work and how to read them with `feedparser` instead of scraping web pages.
- How to add a **time-limited cache** so repeat runs are fast and feeds are not hit every time.
- How to merge sources: different outlets carry the same story, so duplicates must be removed by URL and by title.
- Why **filtering is harder than it looks**: matching "ai" inside "said" showed me why whole-word matching matters.
- How to write **offline tests** against saved sample data, so results are the same every time.
- How to **package a Python project** so `pip install` gives a real command (`newsfeed`).
- How to finish a project properly: README, tests, tag, and a repo others can run.

## 🏗️ How it was built

I planned the architecture first, then built it module by module, reviewing each one and testing it by hand in a terminal.

```text
src/newsfeed/
├── sources.py   # feed names and URLs
├── fetcher.py   # download feeds in parallel (requests) and parse them (feedparser)
├── models.py    # the simple Article object
├── cache.py     # JSON cache with a 15-minute expiry
├── dedupe.py    # remove duplicates by URL and title
├── filters.py   # whole-word topic filter
├── render.py    # Rich terminal output
└── cli.py       # Typer commands and flags
```

**Pipeline:** download each feed → parse into `Article` objects → cache as JSON → merge → sort newest first → de-duplicate → filter by topic → trim to the limit → print with Rich.

**Bugs found while testing, now covered by tests**

- The topic filter matched "ai" inside words like "said".
- Hacker News summaries showed raw text instead of clean text.

It is a command-line tool rather than a library. The modules are small and reusable, but there is no stable public API.

## 🗺️ Plan / what's next

- [x] Four sources with duplicate removal
- [x] On-disk cache and topic filter
- [x] Offline tests and `pip` packaging
- [x] Tagged `v0.1.0`
- [ ] **Category filters:** filter by section (world, tech, business), not only by keyword
- [ ] **Config file for custom sources**, instead of editing `sources.py`
- [ ] **SQLite cache** to keep history and make lookups easier
- [ ] **`--since` flag**, e.g. `--since 2h`

## 📄 License

MIT. See [`LICENSE`](LICENSE).
