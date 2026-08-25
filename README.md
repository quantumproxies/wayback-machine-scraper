# Wayback Machine snapshots API — examples

Archived snapshots of a URL or domain from the Internet Archive's CDX API.

**Live page, full schema & pricing → [quanticdata.io/collectors/wayback-machine-api/](https://quanticdata.io/collectors/wayback-machine-api/)**

Reads the Internet Archive's CDX server and delivers one row per archived capture: timestamp (raw and ISO), the original URL, MIME type, HTTP status, content digest, length and the playback URL. Near-identical captures are collapsed by digest. Match a single page or, with match_prefix, an entire path/domain; filter by date range.

## Quick start (curl)

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/wayback_machine/run \
  -H "Authorization: Bearer $QD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"target": "https://example.com", "max_results": 50}'
```

## Python

See [`example.py`](example.py):

```bash
export QD_API_KEY=qd_live_...   # https://quanticdata.io/
python3 example.py
```

## Inputs

- `target` (string, required) — A page URL or a domain to look up snapshots for.
- `match_prefix` (boolean) — Match every URL under this path/domain, not just the exact URL.
- `from` (string) — Earliest capture, YYYYMMDD (or a longer timestamp).
- `to` (string) — Latest capture, YYYYMMDD.
- `max_results` (integer) — How many snapshots to deliver at most (1–1000). You pay only for delivered snapshots.

## Output — one row per snapshot

| field | type | description |
|---|---|---|
| `rank` | integer | 1-based position (oldest first). |
| `timestamp` | string | Capture timestamp (yyyymmddhhmmss). |
| `captured_at` | string | Capture time (ISO 8601). |
| `original_url` | string | The URL as archived. |
| `mimetype` | string | Captured MIME type. |
| `status_code` | string | HTTP status at capture. |
| `digest` | string | Content digest. |
| `length` | integer | Capture size in bytes. |
| `snapshot_url` | string | Wayback playback URL. |

## Pricing

**$0.0003 per delivered snapshot** ($0.3 per 1,000). A run that delivers nothing costs nothing, and failed rows are never billed. The $2/month free allowance covers roughly 6,666 snapshots — no card required.

## Links

- This collector: https://quanticdata.io/collectors/wayback-machine-api/
- All collectors: https://quanticdata.io/collectors/
- Docs: https://quanticdata.io/docs/
