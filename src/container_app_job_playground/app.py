from __future__ import annotations

import argparse
import logging
import time
from datetime import timedelta

from pytimeparse2 import parse

logger = logging.getLogger(__name__)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Human-readable duration string to future Unix timestamp converter.")
    parser.add_argument(
        "--duration",
        "-d",
        required=True,
        help="Duration string like '3m', '5h', or '3m6h'.",
    )
    return parser


def parse_duration(duration_str: str) -> int | None:
    seconds = parse(duration_str)
    if seconds is None:
        return None
    if isinstance(seconds, timedelta):
        return int(seconds.total_seconds())
    return int(seconds)


def run_logging(seconds: int) -> None:
    logger.info(f"Logging for {seconds} seconds...")
    for _ in range(seconds):
        logger.info("tikk")
        time.sleep(1)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

    parser = create_parser()
    args = parser.parse_args()
    seconds = parse_duration(args.duration)

    if seconds is None:
        parser.error("Could not parse duration. Use formats like '3m', '5h', '1h30m', or '3m6h'.")

    run_logging(seconds)


if __name__ == "__main__":  # pragma: no cover
    main()
