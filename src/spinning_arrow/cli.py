"""Console command dispatch."""

from __future__ import annotations

import sys
from collections.abc import Sequence

from spinning_arrow import phase2, phase2_report, report, run, smoke


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] not in {"smoke", "pilot", "pilot-report", "phase2", "phase2-report"}:
        print(
            "Usage: spinning-arrow {smoke|pilot|pilot-report|phase2|phase2-report} [options]",
            file=sys.stderr,
        )
        return 2
    command = args.pop(0)
    if command == "smoke":
        return smoke.main(args)
    if command == "pilot-report":
        return report.main(args)
    if command == "phase2":
        return phase2.main(args)
    if command == "phase2-report":
        return phase2_report.main(args)
    return run.main(args)
