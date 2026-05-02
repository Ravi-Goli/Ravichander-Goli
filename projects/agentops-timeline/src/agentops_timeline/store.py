from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

APP_DIR = ".agentops-timeline"
CURRENT_FILE = "current-session"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class TimelineStore:
    root: Path

    @property
    def app_dir(self) -> Path:
        return self.root / APP_DIR

    @property
    def sessions_dir(self) -> Path:
        return self.app_dir / "sessions"

    @property
    def current_path(self) -> Path:
        return self.app_dir / CURRENT_FILE

    def init(self) -> None:
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

    def start_session(self, goal: str) -> dict[str, Any]:
        self.init()
        session_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S") + "-" + uuid4().hex[:6]
        session = {
            "id": session_id,
            "goal": goal,
            "started_at": utc_now(),
            "events": [],
        }
        self.save_session(session)
        self.current_path.write_text(session_id + "\n", encoding="utf-8")
        return session

    def get_current_session_id(self) -> str:
        if not self.current_path.exists():
            raise RuntimeError("No active session. Run `agentops start \"your goal\"` first.")
        return self.current_path.read_text(encoding="utf-8").strip()

    def session_path(self, session_id: str) -> Path:
        return self.sessions_dir / f"{session_id}.json"

    def load_session(self, session_id: str | None = None) -> dict[str, Any]:
        self.init()
        resolved_id = session_id or self.get_current_session_id()
        path = self.session_path(resolved_id)
        if not path.exists():
            raise RuntimeError(f"Session not found: {resolved_id}")
        return json.loads(path.read_text(encoding="utf-8"))

    def save_session(self, session: dict[str, Any]) -> None:
        self.init()
        self.session_path(session["id"]).write_text(
            json.dumps(session, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def add_event(self, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
        session = self.load_session()
        event = {
            "id": uuid4().hex[:10],
            "type": event_type,
            "created_at": utc_now(),
            **payload,
        }
        session.setdefault("events", []).append(event)
        self.save_session(session)
        return event


def find_repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists():
            return candidate
    return current


def store_from_cwd() -> TimelineStore:
    root = Path(os.environ.get("AGENTOPS_ROOT", find_repo_root()))
    return TimelineStore(root=root)
