"""Wayback Machine links for a list of dead URLs.

    python rescue_dead_links.py --urls dead_links.txt --out rescued.csv

For each URL in the file (one per line) finds the newest capture archived with
HTTP status 200 and writes its playback link next to it. URLs with no such
capture get an empty link, so you know which ones need another fix.
"""

import argparse

from quanticdata_wayback_machine_scraper import WaybackMachineScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--urls", default="dead_links.txt", help="file with one URL per line")
    parser.add_argument("--out", default="rescued.csv")
    args = parser.parse_args()

    with open(args.urls, encoding="utf-8") as fh:
        urls = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

    wayback = WaybackMachineScraper()
    rows = []
    for url in urls:
        run = wayback.snapshots(url, newest_first=True, status_code="200", max_results=1)
        best = run.rows[0] if len(run) else None
        rows.append({"url": url, "archived_at": best["captured_at"] if best else None,
                     "wayback_url": best["snapshot_url"] if best else None})
        print(f"{url}  ->  {best['snapshot_url'] if best else 'no capture with status 200'}")

    write(rows, args.out)
    found = sum(1 for r in rows if r["wayback_url"])
    print(f"{found} of {len(rows)} URLs have an archived copy; written to {args.out}")


if __name__ == "__main__":
    main()
