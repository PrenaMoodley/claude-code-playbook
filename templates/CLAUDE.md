# <Project name>

<One paragraph: what business process this supports, who uses it, and what
"working" means to them. Example: "Imports POS sales from Simphony every night
and posts summarised journals to Business Central. Finance relies on it for the
daily flash report by 8am.">

## Commands

- Install: `<command>`
- Test: `<command>` (must not call paid or production APIs)
- Lint / format: `<command>`
- Run locally: `<command>`

## Systems this touches

| System | Read / write | Auth | Sandbox? |
|---|---|---|---|
| <e.g. Business Central> | write journals | OAuth client credentials, Entra app `<name>` | yes |
| <e.g. Simphony> | read sales | API key in `SIMPHONY_KEY` | no, use fixtures in `tests/fixtures` |

## Rules

- Money is `Decimal` (Python) or integer cents. Never floats.
- Dates are stored in UTC and shown in Africa/Johannesburg.
- Every job is safe to re-run for the same date. Check before you write.
- Never write to a production system from a test or a local run.
- Never print, log or commit secrets. Read them from environment variables.
- Every new failure mode gets a section in `docs/RUNBOOK.md`.
- Every change gets a line in `CHANGELOG.md` under "Unreleased".

## Where AI is used

<Say which steps call a model and why, and which are deliberately plain code.
If nothing calls a model, say so.>

## Before you finish a task

1. Run the tests and the linter.
2. Run the `code-reviewer` subagent on the change.
3. Update the changelog (`/changelog`) and the runbook if needed.
