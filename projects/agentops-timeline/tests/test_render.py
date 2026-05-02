from agentops_timeline.render import render_pr_notes, render_summary


def test_render_summary_includes_commands_files_and_notes():
    session = {
        "id": "session-1",
        "goal": "fix login",
        "started_at": "2026-01-01T00:00:00+00:00",
        "events": [
            {"type": "command", "command": "pytest -q", "returncode": 0},
            {"type": "snapshot", "files": ["src/auth.py"], "diff_stat": "src/auth.py | 2 ++"},
            {"type": "note", "text": "Added regression coverage"},
            {"type": "risk", "text": "Needs integration test"},
        ],
    }

    output = render_summary(session)

    assert "Goal: fix login" in output
    assert "PASS `pytest -q`" in output
    assert "src/auth.py" in output
    assert "Added regression coverage" in output
    assert "Needs integration test" in output


def test_render_pr_notes_uses_pr_title():
    session = {
        "id": "session-1",
        "goal": "ship feature",
        "started_at": "2026-01-01T00:00:00+00:00",
        "events": [],
    }

    assert render_pr_notes(session).startswith("# PR Notes")
