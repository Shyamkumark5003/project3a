from pathlib import Path

import pytest
from log_analyser.analyser import analyse_file, analyse_lines
from log_analyser.cli import main
from log_analyser.exceptions import LogFileNotFoundError, MalformedLineError
from log_analyser.parser import parse_line

SAMPLE = [
    "2026-10-28 10:00:01 INFO Server started",
    "2026-10-28 10:00:05 ERROR Database timeout",
    "2026-10-28 10:00:09 ERROR Database timeout",
    "2026-10-28 10:01:00 WARNING Disk almost full",
    "garbage line",
    "2026-10-28 10:02:00 ERROR Login failed",
]


def test_parse_valid_line() -> None:
    entry = parse_line("2026-10-28 10:00:05 ERROR Database timeout")
    assert entry.level == "ERROR"
    assert entry.message == "Database timeout"


def test_parse_warn_becomes_warning() -> None:
    assert parse_line("2026-10-28 10:00:05 warn low memory").level == "WARNING"


def test_parse_garbage_raises() -> None:
    with pytest.raises(MalformedLineError):
        parse_line("garbage")


def test_parse_bad_date_raises() -> None:
    with pytest.raises(MalformedLineError):
        parse_line("2026-13-40 10:00:00 INFO bad date")


def test_counts_by_level() -> None:
    summary = analyse_lines(SAMPLE)
    assert summary.counts_by_level == {"INFO": 1, "ERROR": 3, "WARNING": 1}


def test_top_errors() -> None:
    summary = analyse_lines(SAMPLE, top_n=1)
    assert summary.top_errors == [("Database timeout", 2)]


def test_time_range() -> None:
    summary = analyse_lines(SAMPLE)
    assert summary.first_timestamp is not None
    assert summary.last_timestamp is not None
    assert summary.first_timestamp.second == 1
    assert summary.last_timestamp.minute == 2


def test_bad_lines_counted_not_crashing() -> None:
    summary = analyse_lines(SAMPLE)
    assert summary.bad_lines == 1
    assert summary.bad_line_numbers == [5]


def test_empty_input() -> None:
    summary = analyse_lines([])
    assert summary.counts_by_level == {}
    assert summary.first_timestamp is None


def test_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(LogFileNotFoundError):
        analyse_file(tmp_path / "nope.log")


def test_cli_missing_file_returns_2(tmp_path: Path) -> None:
    assert main([str(tmp_path / "nope.log")]) == 2
