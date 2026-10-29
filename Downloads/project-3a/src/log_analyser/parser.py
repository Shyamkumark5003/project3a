"""Turn one text line into a LogEntry."""

import re
from datetime import datetime

from log_analyser.exceptions import MalformedLineError
from log_analyser.models import LogEntry

# Example line: 2026-10-28 10:00:05 ERROR Database timeout
# Change this pattern if your log looks different.
LINE_PATTERN = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})"
    r"\s+\[?(?P<level>DEBUG|INFO|WARN|WARNING|ERROR|CRITICAL)\]?"
    r"\s+(?P<msg>.+?)\s*$",
    re.IGNORECASE,
)


def parse_line(line: str) -> LogEntry:
    """Parse one line or raise MalformedLineError."""
    match = LINE_PATTERN.match(line.strip())
    if match is None:
        raise MalformedLineError(f"Line does not match log format: {line!r}")
    try:
        timestamp = datetime.fromisoformat(match.group("ts").replace("T", " "))
    except ValueError as exc:  # e.g. month 13
        raise MalformedLineError(f"Invalid timestamp: {line!r}") from exc
    level = match.group("level").upper()
    if level == "WARN":
        level = "WARNING"
    return LogEntry(timestamp=timestamp, level=level, message=match.group("msg"))
