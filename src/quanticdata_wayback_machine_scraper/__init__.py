"""Wayback Machine Scraper: Wayback Machine scraper for Python and the command line: archived snapshots of a URL or a whole domain with capture time, HTTP status, MIME type, size, content digest and playback links, filtered by date range, as JSON or CSV. Free and open source; sign in with your QuanticData account, no proxies needed.

    from quanticdata_wayback_machine_scraper import WaybackMachineScraper

    scraper = WaybackMachineScraper()   # saved login (`wayback-machine-scraper login`) or QUANTICDATA_API_KEY
    run = scraper.snapshots(...)   # archived snapshots of a URL or domain
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["WaybackMachineScraper", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class WaybackMachineScraper:
    """Wayback Machine Scraper on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="wayback-machine-scraper/0.1.0 (+https://github.com/quantumproxies/wayback-machine-scraper)", timeout=timeout)

    def snapshots(
        self, target: str,
        *,
        match_prefix: Optional[bool] = None,
        from_: Optional[str] = None,
        to: Optional[str] = None,
        newest_first: Optional[bool] = None,
        status_code: Optional[str] = None,
        mimetype: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Archived snapshots of a URL or domain in the Internet Archive's Wayback Machine: capture time, HTTP status, MIME type, size and content digest, with the playback link and the raw capture link. --match-prefix covers every URL under a path or domain.

        Args:
            target: A page URL or a domain, e.g. quantumproxies.io or https://quanticdata.io/docs/.
            match_prefix: Match every URL under this path or domain, not just the exact URL.
            from_: Earliest capture, YYYYMMDD (or a longer timestamp).
            to: Latest capture, YYYYMMDD.
            newest_first: Return the most recent captures instead of the oldest.
            status_code: Only captures with this HTTP status, e.g. 200.
            mimetype: Only captures of this MIME type, e.g. text/html.
            max_results: How many snapshots to deliver at most (1–1000). You pay only for delivered snapshots.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 1000 rows, one per snapshot: see ``types.WaybackMachineRow``.
        """
        payload = {
            "target": target,
            "match_prefix": match_prefix,
            "from": from_,
            "to": to,
            "newest_first": newest_first,
            "status_code": status_code,
            "mimetype": mimetype,
            "max_results": max_results,
        }
        return self.client.run_collector("wayback_machine", payload, wait=wait, timeout=timeout)
