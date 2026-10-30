"""Every URL archived under a domain, with its first and last capture.

    python archived_urls.py quantumproxies.io --from 20250101 --out archived_urls.csv

Reads the captures of every URL under the domain (match_prefix), groups them
by URL and writes one row per URL: first and last capture, number of captures
and the HTTP statuses seen. Useful before a migration, to build a redirect map
of the pages that once existed.
"""

import argparse

from quanticdata_wayback_machine_scraper import WaybackMachineScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("domain")
    parser.add_argument("--from", dest="since", help="earliest capture, YYYYMMDD")
    parser.add_argument("--to", dest="until", help="latest capture, YYYYMMDD")
    parser.add_argument("--max", type=int, default=1000, help="captures to read (max 1000)")
    parser.add_argument("--out", default="archived_urls.csv")
    args = parser.parse_args()

    wayback = WaybackMachineScraper()
    run = wayback.snapshots(args.domain, match_prefix=True, from_=args.since, to=args.until, max_results=args.max)

    urls = {}
    for c in run:
        url = c.get("original_url")
        if not url:
            continue
        entry = urls.setdefault(url, {"url": url, "first": c, "last": c, "captures": 0, "statuses": set()})
        entry["captures"] += 1
        entry["statuses"].add(c.get("status_code") or "-")
        if c["timestamp"] < entry["first"]["timestamp"]:
            entry["first"] = c
        if c["timestamp"] > entry["last"]["timestamp"]:
            entry["last"] = c

    rows = [{"url": e["url"], "first_capture": e["first"]["captured_at"], "last_capture": e["last"]["captured_at"],
             "captures": e["captures"], "statuses": "; ".join(sorted(e["statuses"])),
             "last_snapshot": e["last"]["snapshot_url"]} for e in urls.values()]
    rows.sort(key=lambda r: r["url"])

    write(rows, args.out)
    print(f"{len(rows)} URLs from {len(run)} captures written to {args.out}")


if __name__ == "__main__":
    main()
