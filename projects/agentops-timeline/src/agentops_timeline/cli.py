from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from agentops_timeline.git_tools import get_git_snapshot
from agentops_timeline.render import render_pr_notes, render_summary
from agentops_timeline.store import store_from_cwd


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agentops",
        description="Record local timelines for AI-assisted coding sessions.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Create the local .agentops-timeline directory")

    start = subparsers.add_parser("start", help="Start a new coding session")
    start.add_argument("goal", help="Goal for this AI-assisted coding session")

    for name, help_text in [
        ("note", "Record an observation"),
        ("decision", "Record a decision"),
        ("risk", "Record a risk"),
        ("next-step", "Record a next step"),
    ]:
        command = subparsers.add_parser(name, help=help_text)
        command.add_argument("text", help=help_text)

    run = subparsers.add_parser("run", help="Run a command and capture its result")
    run.add_argument("cmd", nargs=argparse.REMAINDER, help="Command to run after --")

    subparsers.add_parser("snapshot", help="Record current git status and diff stat")
    subparsers.add_parser("summary", help="Print a Markdown session summary")

    export = subparsers.add_parser("export-pr-notes", help="Write Markdown PR notes")
    export.add_argument("--output", "-o", default="PR_NOTES.md", help="Output file path")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    store = store_from_cwd()

    try:
        if args.command == "init":
            store.init()
            print(f"Initialized {store.app_dir}")
            return 0

        if args.command == "start":
            session = store.start_session(args.goal)
            print(f"Started session {session['id']}")
            return 0

        if args.command in {"note", "decision", "risk", "next-step"}:
            event_type = args.command.replace("-", "_")
            store.add_event(event_type, {"text": args.text})
            print(f"Recorded {args.command}")
            return 0

        if args.command == "run":
            return _run_command(args.cmd, store)

        if args.command == "snapshot":
            snapshot = get_git_snapshot(store.root)
            store.add_event("snapshot", snapshot)
            print(f"Recorded snapshot with {len(snapshot.get('files', []))} changed file(s)")
            return 0

        if args.command == "summary":
            print(render_summary(store.load_session()), end="")
            return 0

        if args.command == "export-pr-notes":
            output = Path(args.output)
            output.write_text(render_pr_notes(store.load_session()), encoding="utf-8")
            print(f"Wrote {output}")
            return 0

    except RuntimeError as error:
        print(f"agentops: {error}", file=sys.stderr)
        return 1

    parser.error(f"Unknown command: {args.command}")
    return 2


def _run_command(cmd: list[str], store) -> int:
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]
    if not cmd:
        raise RuntimeError("Provide a command after `agentops run --`.")

    process = subprocess.run(
        cmd,
        cwd=store.root,
        text=True,
        capture_output=True,
        check=False,
    )
    store.add_event(
        "command",
        {
            "command": " ".join(cmd),
            "returncode": process.returncode,
            "stdout_tail": process.stdout[-4000:],
            "stderr_tail": process.stderr[-4000:],
        },
    )

    if process.stdout:
        print(process.stdout, end="")
    if process.stderr:
        print(process.stderr, end="", file=sys.stderr)
    return process.returncode


if __name__ == "__main__":
    raise SystemExit(main())
