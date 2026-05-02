from __future__ import annotations

from collections import defaultdict
from typing import Any


def render_summary(session: dict[str, Any]) -> str:
    events = session.get("events", [])
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        grouped[event.get("type", "unknown")].append(event)

    lines = [
        "# AgentOps Timeline Summary",
        "",
        f"Goal: {session.get('goal', 'No goal recorded')}",
        f"Session: `{session.get('id')}`",
        f"Started: {session.get('started_at')}",
        "",
    ]

    _append_commands(lines, grouped.get("command", []))
    _append_snapshot(lines, grouped.get("snapshot", []))
    _append_text_events(lines, "Decisions", grouped.get("decision", []))
    _append_text_events(lines, "Notes", grouped.get("note", []))
    _append_text_events(lines, "Risks", grouped.get("risk", []))
    _append_text_events(lines, "Next Steps", grouped.get("next_step", []))

    if len(lines) <= 6:
        lines.extend(["No events recorded yet.", ""])

    return "\n".join(lines).rstrip() + "\n"


def render_pr_notes(session: dict[str, Any]) -> str:
    summary = render_summary(session)
    return summary.replace("# AgentOps Timeline Summary", "# PR Notes", 1)


def _append_commands(lines: list[str], events: list[dict[str, Any]]) -> None:
    if not events:
        return
    lines.extend(["## Commands", ""])
    for event in events:
        status = "PASS" if event.get("returncode") == 0 else "FAIL"
        lines.append(f"- {status} `{event.get('command')}`")
    lines.append("")


def _append_snapshot(lines: list[str], events: list[dict[str, Any]]) -> None:
    if not events:
        return
    latest = events[-1]
    files = latest.get("files", [])
    lines.extend(["## Changed Files", ""])
    if files:
        for file_name in files:
            lines.append(f"- {file_name}")
    else:
        lines.append("- No changed files detected")
    diff_stat = latest.get("diff_stat")
    if diff_stat:
        lines.extend(["", "```text", str(diff_stat), "```"])
    lines.append("")


def _append_text_events(lines: list[str], title: str, events: list[dict[str, Any]]) -> None:
    if not events:
        return
    lines.extend([f"## {title}", ""])
    for event in events:
        lines.append(f"- {event.get('text')}")
    lines.append("")
