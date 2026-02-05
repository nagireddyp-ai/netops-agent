from __future__ import annotations

import argparse

from rich.console import Console

from .db import NetOpsDatabase
from .workflows import NetOpsWorkflow, RunContext


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NetOps Agent (local synthetic demo)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run the end-to-end workflow")
    run_parser.add_argument("--seed", type=int, default=42)
    run_parser.add_argument("--db-path", default="outputs/netops.duckdb")
    run_parser.add_argument("--log-path", default="outputs/netops.log")
    run_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print execution logs to the console in addition to writing the log file.",
    )

    show_parser = subparsers.add_parser("show-db", help="Show DuckDB tables")
    show_parser.add_argument("--db-path", default="outputs/netops.duckdb")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    console = Console()

    if args.command == "run":
        workflow = NetOpsWorkflow(
            RunContext(
                seed=args.seed,
                db_path=args.db_path,
                log_path=args.log_path,
                verbose=args.verbose,
            )
        )
        workflow.run()
    elif args.command == "show-db":
        db = NetOpsDatabase(args.db_path)
        tables = db.show_tables()
        for name, df in tables.items():
            console.rule(f"{name}")
            console.print(df)


if __name__ == "__main__":
    main()
