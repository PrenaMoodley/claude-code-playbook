"""Hooks are code that guards every session, so they get tests like any other code."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOKS = Path(__file__).resolve().parents[1] / ".claude" / "hooks"


def run_hook(name: str, tool: str, tool_input: dict) -> int:
    payload = json.dumps({"tool_name": tool, "tool_input": tool_input})
    return subprocess.run(
        [sys.executable, str(HOOKS / name)], input=payload, text=True, capture_output=True
    ).returncode


@pytest.mark.parametrize(
    "tool,tool_input,blocked",
    [
        ("Read", {"file_path": "/repo/.env"}, True),
        ("Read", {"file_path": "/repo/.env.production"}, True),
        ("Read", {"file_path": "/repo/certs/server.pem"}, True),
        ("Read", {"file_path": "/repo/.env.example"}, False),
        ("Read", {"file_path": "/repo/src/environment.py"}, False),
        ("Bash", {"command": "cat .env"}, True),
        ("Bash", {"command": "echo $ANTHROPIC_API_KEY"}, True),
        ("Bash", {"command": "printenv"}, True),
        ("Bash", {"command": "python -m venv .venv && pytest -q"}, False),
        ("Bash", {"command": "cp .env.example .env.example.bak"}, False),
    ],
)
def test_protect_secrets(tool, tool_input, blocked):
    assert run_hook("protect_secrets.py", tool, tool_input) == (2 if blocked else 0)


@pytest.mark.parametrize(
    "command,blocked",
    [
        ('psql "$DB" -c "DROP TABLE invoices"', True),
        ('psql "$DB" -c "TRUNCATE invoices"', True),
        ('psql "$DB" -c "DELETE FROM invoices"', True),
        ('psql "$DB" -c "UPDATE invoices SET status = \'paid\'"', True),
        ('psql "$DB" -c "DELETE FROM invoices WHERE number = \'INV-1\'"', False),
        ("psql \"$DB\" -c \"UPDATE invoices SET status = 'open' WHERE number = 'INV-1'\"", False),
        ('psql "$DB" -c "SELECT count(*) FROM invoices"', False),
        ("grep -r 'DROP TABLE' docs/", False),  # not a database client
    ],
)
def test_guard_sql(command, blocked):
    assert run_hook("guard_sql.py", "Bash", {"command": command}) == (2 if blocked else 0)


def test_guard_sql_ignores_other_tools():
    assert run_hook("guard_sql.py", "Write", {"file_path": "x.sql", "content": "DROP TABLE x"}) == 0
