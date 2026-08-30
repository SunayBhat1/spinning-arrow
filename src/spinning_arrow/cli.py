"""Console command dispatch."""

from __future__ import annotations

import sys
from collections.abc import Sequence

from spinning_arrow import run, smoke


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] not in {"smoke", "pilot"}:
        print("Usage: spinning-arrow {smoke|pilot} [options]", file=sys.stderr)
        return 2
    command = args.pop(0)
    if command == "smoke":
        return smoke.main(args)
    return run.main(args)
