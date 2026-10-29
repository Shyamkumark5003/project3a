"""Data containers."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class LogEntry:
    """One valid log line."""

    timestamp: datetime
    level: str
    message: str


@dataclass
class Summary:
    """Result of analysing a whole log."""

    counts_by_level: dict[str, int] = field(default_factory=dict)
    top_errors: list[tuple[str, int]] = field(default_factory=list)
    first_timestamp: datetime | None = None
    last_timestamp: datetime | None = None
    total_lines: int = 0
    bad_lines: int = 0
    bad_line_numbers: list[int] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-friendly dict (datetimes become ISO strings)."""
        return {
            "counts_by_level": self.counts_by_level,
            "top_errors": [{"message": msg, "count": n} for msg, n in self.top_errors],
            "time_range": {
                "first": _iso(self.first_timestamp),
                "last": _iso(self.last_timestamp),
            },
            "total_lines": self.total_lines,
            "bad_lines": self.bad_lines,
            "bad_line_numbers": self.bad_line_numbers,
        }


def _iso(value: datetime | None) -> str | None:
    return value.isoformat(sep=" ") if value else None
