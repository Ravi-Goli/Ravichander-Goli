from agentops_timeline.store import TimelineStore


def test_store_starts_session_and_records_event(tmp_path):
    store = TimelineStore(root=tmp_path)

    session = store.start_session("fix auth")
    event = store.add_event("note", {"text": "found auth module"})
    loaded = store.load_session()

    assert session["goal"] == "fix auth"
    assert event["type"] == "note"
    assert loaded["events"][0]["text"] == "found auth module"
    assert (tmp_path / ".agentops-timeline" / "current-session").exists()
