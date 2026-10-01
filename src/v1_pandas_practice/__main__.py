"""Command-line entry point for V1 pandas practice."""

from __future__ import annotations

import argparse
from pathlib import Path

from v1_pandas_practice import load_traces
from v1_pandas_practice.checker import QUESTS, check_answers


def main() -> None:
    parser = argparse.ArgumentParser(description="Pandas quests with real V1 traces")
    parser.add_argument("command", nargs="?", choices=["quests", "data", "check"])
    parser.add_argument(
        "quests", nargs="*", help="Optional quest function names to check"
    )
    args = parser.parse_args()
    if args.command == "data":
        traces = load_traces()
        print(traces.head().to_string(index=False))
        print(f"\n{len(traces):,} frames, {traces['cell_id'].nunique()} cells")
    elif args.command == "check":
        answer_file = Path.cwd() / "practice.py"
        if not answer_file.exists():
            parser.error("Run from the repository root, where practice.py lives")
        try:
            complete = check_answers(answer_file, args.quests)
        except ValueError as error:
            parser.error(str(error))
        raise SystemExit(0 if complete else 1)
    else:
        print("V1 pandas practice: six quests, four cells, real calcium and spikes.\n")
        for number, (name, (title, _, _)) in enumerate(QUESTS.items(), 1):
            print(f"{number}. {title}  ({name})")
        print("\nEdit practice.py, then run ./start.sh check to see your progress.")
        print("Use ./start.sh data to peek at the bundled traces.")


if __name__ == "__main__":
    main()
