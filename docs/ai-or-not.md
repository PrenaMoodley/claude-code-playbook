# AI, a script, a flow or a setting?

Most automation requests don't need a language model. Choosing AI where a
script would do adds cost, latency, and answers that can differ between runs.
Choosing a script where the input is messy produces something that breaks on
every new format. I work down this list and stop at the first option that fits.

## 1. Can the system already do it?

A configuration change, a built-in report, an approval workflow, a scheduled
export. Check the ERP, CRM or Microsoft 365 settings before writing anything.
Cheapest to build, and someone else maintains it.

## 2. Is it a simple trigger and action inside Microsoft 365?

"When a file lands in this SharePoint folder, email the team." "When a form is
submitted, add a row and post in Teams." That's **Power Automate**. The business
can see and adjust it, and it runs under existing licences.

## 3. Is the input structured and the logic fixed?

CSV exports, API responses, database rows. Totals, VAT, matching on keys,
reconciliations, moving data between systems. That's **a script or a small
service** with tests. Exact, repeatable, cheap to run, easy to audit.

## 4. Is the input unstructured, or does it need judgement about language?

Emailed and scanned documents in many layouts, free-text descriptions to
classify, a question in plain English about business data. That's where
**the Claude API** earns its place. Even then:

- Keep the AI step narrow: it reads, extracts, classifies or suggests.
- Do every calculation and every rule check in ordinary code afterwards.
- Put a person in the loop wherever a wrong answer costs money.
- Use structured outputs, so the response always fits a schema.
- Use the Batch API for anything that can wait, and prompt caching for repeated context.
- Measure: log token usage and spot-check outputs against known answers.

## 5. Does someone need to explore data or systems interactively?

Give Claude **read-only tools** through an MCP server rather than database
credentials or a "run any query" tool, so access stays scoped and auditable.

## Examples

| Request | Choice | Why |
|---|---|---|
| Email the daily sales report to managers | System setting or Power Automate | Built-in scheduling exists |
| Post nightly POS totals to the ledger | Script | Structured data, fixed rules, must be exact |
| Match bank receipts to invoices | Script, with a review queue | Exact rules; people handle the leftovers |
| Capture customer POs that arrive as PDFs and emails | Claude API + script checks | Layouts vary; totals still checked in code |
| "Which orders are late and why?" from managers | Claude + read-only MCP server | Open questions over live data |
