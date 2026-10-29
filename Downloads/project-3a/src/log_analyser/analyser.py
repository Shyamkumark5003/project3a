"""Count levels, top errors and time range. Bad lines never crash it."""

import logging
from collections import Counter
from collections.abc import Iterable
from pathlib import Path

from log_analyser.exceptions import LogFileNotFoundError, MalformedLineError
from log_analyser.models import Summary
from log_analyser.parser import parse_line

logger = logging.getLogger(__name__)


def analyse_lines(lines: Iterable[str], top_n: int = 5) -> Summary:
    levels: Counter[str] = Counter()
    errors: Counter[str] = Counter()
    times = []
    summary = Summary()

    for line_no, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        summary.total_lines += 1
        try:
            entry = parse_line(line)
        except MalformedLineError:
            summary.bad_lines += 1
            summary.bad_line_numbers.append(line_no)
            logger.warning("Skipping bad line %d", line_no)
            continue
        levels[entry.level] += 1
        if entry.level in ("ERROR", "CRITICAL"):
            errors[entry.message] += 1
        times.append(entry.timestamp)

    summary.counts_by_level = dict(levels)
    summary.top_errors = errors.most_common(top_n)
    if times:
        summary.first_timestamp = min(times)
        summary.last_timestamp = max(times)
    return summary


def analyse_file(path: Path, top_n: int = 5) -> Summary:
    try:
        with path.open(encoding="utf-8", errors="replace") as handle:
            return analyse_lines(handle, top_n=top_n)
    except OSError as exc:
        raise LogFileNotFoundError(f"Cannot read log file: {path}") from exc
