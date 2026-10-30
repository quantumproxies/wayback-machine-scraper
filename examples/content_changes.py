"""When a page actually changed, according to the Wayback Machine.

    python content_changes.py https://quantumproxies.io/ --from 20250101 --out changes.csv

Reads the captures of one URL (oldest first, HTTP 200 only) and keeps those
whose content digest differs from the previous capture: one row per version
of the page, with its date, size and playback link.
"""

import argparse

from quanticdata_wayback_machine_scraper import WaybackMachineScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("url")
    parser.add_argument("--from", dest="since", help="earliest capture, YYYYMMDD")
    parser.add_argument("--to", dest="until", help="latest capture, YYYYMMDD")
    parser.add_argument("--max", type=int, default=1000, help="captures to read (max 1000)")
    parser.add_argument("--out", default="changes.csv")
    args = parser.parse_args()

    wayback = WaybackMachineScraper()
    run = wayback.snapshots(args.url, from_=args.since, to=args.until, status_code="200", max_results=args.max)

    versions = []
    last_digest = None
    for capture in run:
        digest = capture.get("digest")
        if digest and digest != last_digest:
            versions.append(capture)
            last_digest = digest
    for v in versions:
        print(f"{v['captured_at']}  {v.get('length') or '':>8}  {v['snapshot_url']}")

    write(versions, args.out)
    print(f"{len(versions)} distinct versions in {len(run)} captures, written to {args.out}")


if __name__ == "__main__":
    main()
