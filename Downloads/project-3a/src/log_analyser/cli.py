"""Command-line entry point."""

import argparse
import json
import logging
import sys
from pathlib import Path

from log_analyser.analyser import analyse_file
from log_analyser.exceptions import LogAnalyserError

logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Summarise a log file as JSON.")
    parser.add_argument("logfile", type=Path)
    parser.add_argument("--top", type=int, default=5)
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.WARNING, stream=sys.stderr)
    try:
        summary = analyse_file(args.logfile, top_n=args.top)
    except LogAnalyserError as exc:
        logger.error("%s", exc)
        return 2

    sys.stdout.write(json.dumps(summary.to_dict(), indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
