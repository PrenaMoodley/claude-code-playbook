# claude-code-playbook

**The Claude Code setup I use for business-systems work: skills, slash commands, subagents and hooks, with tests.**

Claude Code is my main development environment. This repository is the reusable
part of that setup, aimed at the work I do most: integrations, automations,
reconciliations and internal tools for finance and operations teams.

## What's inside

```
.claude/
  settings.json                 hooks wired up, secret files denied
  hooks/
    protect_secrets.py          PreToolUse: blocks reading .env/keys and printing env vars
    guard_sql.py                PreToolUse: blocks DROP, TRUNCATE, and DELETE/UPDATE without WHERE
    format_python.py            PostToolUse: ruff format + lint every edited .py; lint errors go back to Claude
  skills/
    write-scope/                business request -> one-page scope a stakeholder can approve
    write-runbook/              deployed system -> on-call runbook with copy-paste fixes
    reconcile-files/            two exports -> exact reconciliation workbook (script does the maths)
  commands/
    changelog.md                /changelog: changes -> plain-language changelog entries
    handover.md                 /handover [audience]: handover note for the next owner
  agents/
    code-reviewer.md            read-only review for wrong results, integration failures, security
    integration-researcher.md   researches an unfamiliar API, writes an integration brief
templates/CLAUDE.md             starting CLAUDE.md for a business-systems project
docs/ai-or-not.md               how I decide between AI, a script, Power Automate or a setting
tests/                          tests for the hooks and the reconciliation script
```

## Principles

1. **CLAUDE.md is the contract.** Commands, systems touched (read or write),
   and the rules that matter: `Decimal` money, re-runnable jobs, no production
   writes from local runs. See the [template](templates/CLAUDE.md).
2. **Guardrails are code, not reminders.** Hooks enforce what must never
   happen (reading secrets, destructive SQL) and what must always happen
   (formatting and linting). They're tested like any other code.
3. **The model reads and drafts; scripts calculate.** The reconciliation skill
   runs a Python script for the maths and asks Claude to explain the exceptions.
   See [`docs/ai-or-not.md`](docs/ai-or-not.md).
4. **Subagents for focused, read-only review.** Reviewers get read tools only
   and report findings; they don't edit.
5. **Documentation is part of done.** Scopes before building, runbooks and
   changelogs after. Skills make that the easy path.

## Use it

Copy into a project (or into `~/.claude/` to use everywhere):

```bash
cp -r .claude /path/to/project/
cp templates/CLAUDE.md /path/to/project/CLAUDE.md   # then fill it in
```

Hooks need Python 3.10+ on the `PATH`, and `ruff` for the formatting hook (`pip install ruff`).

Run the tests:

```bash
pip install pytest openpyxl
python -m pytest -q
```

## Where these are used

- [po-intake-ai](https://github.com/PrenaMoodley/po-intake-ai): Claude API tool use, structured outputs, Batch API and prompt caching for purchase-order intake.
- [erp-mcp-server](https://github.com/PrenaMoodley/erp-mcp-server): read-only MCP server over a PostgreSQL ERP.
- [recon-dashboard](https://github.com/PrenaMoodley/recon-dashboard): FastAPI + PostgreSQL + Next.js bank reconciliation.

## Licence

MIT
