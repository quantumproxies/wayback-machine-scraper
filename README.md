# Wayback Machine Scraper

[![ci](https://github.com/quantumproxies/wayback-machine-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/wayback-machine-scraper/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Pull the archive history of a URL or a domain from the Wayback Machine, from Python or the command line: every capture with its time, HTTP status, MIME type, size and content digest, plus the playback link and the raw capture link, as JSON or CSV. Filter by date range, status code or MIME type, or cover every URL of a domain with --match-prefix. The code is free and open source (MIT). It runs on the QuanticData Data API: sign in once and run a URL.

```bash
pip install git+https://github.com/quantumproxies/wayback-machine-scraper
wayback-machine-scraper login
wayback-machine-scraper snapshots quantumproxies.io --from 20250101 -o snapshots.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=wayback-machine-scraper).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `wayback-machine-scraper snapshots` | URL or domain | Capture time, status, MIME type, size, digest, playback and raw links, 10 fields per row ([fields and price](https://quanticdata.io/collectors/wayback-machine-api/?utm_source=github&utm_medium=readme&utm_campaign=wayback-machine-scraper)) | up to 1000 |

Dates are `YYYYMMDD` (or a longer timestamp): `--from 20250101 --to 20251231`. Captures come oldest first; `--newest-first` reverses the order. In Python the lower bound is written `from_`, because `from` is a reserved word; the upper bound stays `to`.

## Sample output

A real row from `wayback-machine-scraper snapshots quantumproxies.io --from 20250101 --max-results 3` (2026-10-23):

```json
{
  "rank": 1,
  "digest": "BPHCWF735B4YFOOZQN36ZTPF46F56E2S",
  "length": 5712,
  "raw_url": "https://web.archive.org/web/20250321164954id_/http://quantumproxies.io/",
  "mimetype": "text/html",
  "timestamp": "20250321164954",
  "captured_at": "2025-03-21T16:49:54Z",
  "status_code": "200",
  "original_url": "http://quantumproxies.io/",
  "snapshot_url": "https://web.archive.org/web/20250321164954/http://quantumproxies.io/"
}
```

## Python

```python
from quanticdata_wayback_machine_scraper import WaybackMachineScraper

wayback = WaybackMachineScraper()  # saved login, or QUANTICDATA_API_KEY

captures = wayback.snapshots("quantumproxies.io", from_="20250101", to="20251231", max_results=100)
for c in captures:
    print(c["captured_at"], c["status_code"], c["length"], c["snapshot_url"])
captures.to_csv("quantumproxies_captures.csv")

pages = wayback.snapshots("quantumproxies.io", match_prefix=True, newest_first=True,
                          status_code="200", mimetype="text/html", max_results=500)
print(len({p["original_url"] for p in pages}), "distinct pages archived")
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Page change history**: List the captures of a page and keep only those whose content digest differs from the previous one: the dates the page actually changed, each with its playback link. See [`examples/content_changes.py`](examples/content_changes.py).
- **Archived URL inventory**: Every URL archived under a domain with its first and last capture and capture count, for site migrations, redirect maps and content audits. See [`examples/archived_urls.py`](examples/archived_urls.py).
- **Dead link rescue**: For a list of broken URLs, find the newest capture archived with status 200 and write its Wayback Machine link next to each one. See [`examples/rescue_dead_links.py`](examples/rescue_dead_links.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `wayback-machine-scraper run <id> -o out.csv` collects it later.

### `wayback-machine-scraper snapshots`

Archived snapshots of a URL or domain in the Internet Archive's Wayback Machine: capture time, HTTP status, MIME type, size and content digest, with the playback link and the raw capture link. --match-prefix covers every URL under a path or domain.

```
wayback-machine-scraper snapshots TARGET [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `TARGET` | string |  | A page URL or a domain, e.g. quantumproxies.io or https://quanticdata.io/docs/. |
| `--match-prefix` | boolean | `False` | Match every URL under this path or domain, not just the exact URL. |
| `--from` | string |  | Earliest capture, YYYYMMDD (or a longer timestamp). |
| `--to` | string |  | Latest capture, YYYYMMDD. |
| `--newest-first` | boolean | `False` | Return the most recent captures instead of the oldest. |
| `--status-code` | string |  | Only captures with this HTTP status, e.g. 200. |
| `--mimetype` | string |  | Only captures of this MIME type, e.g. text/html. |
| `--max-results` | integer | `50` | How many snapshots to deliver at most (1–1000). You pay only for delivered snapshots. |

## Output fields

<details><summary><code>wayback-machine-scraper snapshots</code>: 10 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position (oldest first, or newest first with newest_first). |
| `timestamp` | string | Capture timestamp (yyyymmddhhmmss). |
| `captured_at` | string or null | Capture time (ISO 8601). |
| `original_url` | string or null | The URL as archived. |
| `mimetype` | string or null | Captured MIME type. |
| `status_code` | string or null | HTTP status at capture. |
| `digest` | string or null | Content digest of the capture; two captures with the same digest hold the same content. |
| `length` | integer or null | Capture size in bytes. |
| `snapshot_url` | string or null | Wayback Machine playback URL. |
| `raw_url` | string or null | The capture exactly as archived: no toolbar, links not rewritten. |

</details>

## Sign-in and API keys

- `wayback-machine-scraper login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `wayback-machine-scraper login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `wayback-machine-scraper login --api-key`.
- `wayback-machine-scraper logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=wayback-machine-scraper).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/wayback_machine/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"target": "quantumproxies.io", "from": "20250101", "max_results": 3}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=wayback-machine-scraper) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=wayback-machine-scraper) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this Wayback Machine scraper free?**

The code is free and MIT-licensed. Scraping runs on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need proxies or a headless browser?**

No. You send a URL or a domain and get one row per capture back; the archive lookups run on QuanticData's side.

**Can I list every archived page of a domain?**

Yes. --match-prefix matches every URL under the domain or path. Add --from and --to for a period, --status-code 200 and --mimetype text/html to keep the pages that were archived as HTML.

**How many snapshots can one run return?**

Up to 1,000 snapshots per run, 50 by default: raise it with --max-results and you pay only for what is delivered. For more, split the period with --from and --to.

**What is the difference between snapshot_url and raw_url?**

snapshot_url opens the capture in the Wayback Machine player. raw_url is the capture exactly as archived, with no toolbar and links not rewritten: the one to parse or to compare.

**Can I export to CSV?**

Add -o snapshots.csv (or .json, .jsonl) and the file opens cleanly in Excel or Google Sheets. In Python every Run also has to_csv() and to_dataframe().

## Related scrapers

- [Web Scraper API](https://github.com/quantumproxies/web-scraper-api): Web scraper API for Python and the command line.
- [WHOIS API](https://github.com/quantumproxies/whois-api): WHOIS API and DNS lookup API for Python and the command line.
- [Subdomain Finder](https://github.com/quantumproxies/subdomain-finder): Subdomain finder for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=wayback-machine-scraper).
