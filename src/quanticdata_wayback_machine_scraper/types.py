"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class WaybackMachineRow(TypedDict, total=False):
    """One row of `wayback-machine-scraper snapshots` (wayback_machine v1.1.0)."""

    rank: int
    """1-based position (oldest first, or newest first with newest_first)."""
    timestamp: str
    """Capture timestamp (yyyymmddhhmmss)."""
    captured_at: Optional[str]
    """Capture time (ISO 8601)."""
    original_url: Optional[str]
    """The URL as archived."""
    mimetype: Optional[str]
    """Captured MIME type."""
    status_code: Optional[str]
    """HTTP status at capture."""
    digest: Optional[str]
    """Content digest of the capture; two captures with the same digest hold the same content."""
    length: Optional[int]
    """Capture size in bytes."""
    snapshot_url: Optional[str]
    """Wayback Machine playback URL."""
    raw_url: Optional[str]
    """The capture exactly as archived: no toolbar, links not rewritten."""
