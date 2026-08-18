# A custom timer: give it a short text and a duration, and it blocks until
# the time is up, then prints the reminder with a terminal alert. Meant for
# "remind me later" or "tell me when to stop" moments during work.

import re
import time

# Matches things like "20m", "1h", "45s": one or more digits, followed by
# exactly one unit letter, nothing else (^...$ pins it to the whole string).
_DURATION_PATTERN = re.compile(r"^(\d+)([smh])$")

# How many seconds each unit letter is worth.
_UNIT_SECONDS = {"s": 1, "m": 60, "h": 3600}


def parse_duration(value: str) -> int:
    match = _DURATION_PATTERN.match(value)
    if match is None:
        raise ValueError(f"invalid duration '{value}': expected formats like 20m, 1h, 45s")

    amount, unit = match.groups()
    return int(amount) * _UNIT_SECONDS[unit]


def run(text: str, seconds: int) -> None:
    print(f'Reminder "{text}" scheduled in {seconds}s.')

    # Waiting and alerting are two separate, sequential steps on purpose:
    # in v2 (background mode), this same pair could run inside a detached
    # process without touching the parsing/argparse side of things at all.
    time.sleep(seconds)
    print(f'\a\nTime is up: "{text}"')
