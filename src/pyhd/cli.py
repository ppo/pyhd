#!/usr/bin/env python3
"""
Human Design Library: CLI entry point.
"""
import argparse
import sys
from datetime import UTC, datetime

from pyhd import Chart
from pyhd.utils.debug import debug


def parse_datetime_arg(arg: str) -> datetime:
    """Parse the arg string into an aware datetime.

    It supports any string format handled by Python's `datetime.fromisoformat()`.
    If a timezone is specified, it converts it to UTC.
    If not, it assumes the value is in UTC.
    """
    dt = datetime.fromisoformat(arg)
    dt = (dt.astimezone(UTC) if dt.tzinfo  # Aware => convert to UTC.
          else dt.replace(tzinfo=UTC))     # Naive => set as UTC.
    return dt


def parse_args():
    parser = argparse.ArgumentParser(description="PyHD – BodyGraph calculator.")
    parser.add_argument("birth_time", type=parse_datetime_arg,
        help="Birth date/time. Format: 'YYYY-MM-DD HH:MM[:SS][±HH:MM]'")

    args = parser.parse_args()

    return args


def main():
    args = parse_args()
    chart = Chart(args.birth_time)
    # debug(chart.to_model())
    # debug(chart.to_dict())
    chart.print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
