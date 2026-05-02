.PHONY: install test demo

install:
	python3 -m pip install -e .

test:
	python3 -m pytest -q

demo:
	agentops init
	agentops start "demo AI coding session"
	agentops note "Investigated the target files and captured useful context."
	agentops decision "Keep the MVP dependency-free for easy installation."
	agentops risk "GitHub API integration is not implemented yet."
	agentops snapshot
	agentops summary
