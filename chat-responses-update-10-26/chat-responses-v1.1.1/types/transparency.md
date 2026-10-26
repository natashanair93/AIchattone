---
type: transparency
version: 1.0.0
component: step list / trace summary
situation: success (or the situation of the step being explained)
---

# Transparency

Shows what the assistant actually did — the steps, tools, sources, and decisions behind a result — at a density the user can skim and a depth they can audit.

## Use when

- A response came from a run that touched ≥2 steps, tools, or sources.
- The user asks "what did you do", "how did you get that", "why", or "which source".
- A result is surprising, low-confidence, or high-stakes, and the path to it matters.
- An agent acted on the user's behalf (sent, wrote, changed something).

## Don't use when

- The response was a single model call with no tools — nothing to show; a direct answer with evidence is enough.
- Work is still in flight → `progress.md`.
- The point is *evidence for a claim* rather than *steps taken* → the evidence component on a direct answer.

## Anatomy

1. **Summary line** (required) — what happened in one sentence: "3 steps · 9s · $0.02 · all ran ok" or "4 steps · failed at step 3".
2. **Step list** (required) — one line per step: name (exact), outcome, ≤80-char summary, duration, cost. Passing steps collapsed; failed, skipped, stopped, or surprising steps expanded.
3. **Decisions** (optional) — where the agent chose between paths (which tool, which branch, which document), one line each: what it chose and the reason, only when the reason isn't obvious from the step name.
4. **Sources used** (optional) — evidence components for retrieved documents or data.
5. **Drill-in** (required, structural) — every step, including passing ones, opens to its full input and output.

## Length

Summary + one line per step visible. Everything else on demand. A 12-step run is 12 short lines, not 12 paragraphs.

## Tone

Neutral. The step list is a record, not a story. Expanded failures take the error's tone.

## Rules

1. **Summary always, detail on demand, failures inline.** Passing steps collapse to one line; anything not-ok expands.
2. Every step is drillable, including passing ones — a passing step can still return a wrong answer, and the user must be able to check it.
3. Step names are the platform's exact names for those steps, matching the canvas, trace, and logs.
4. Outcomes use only `ok`, `failed`, `skipped`, `stopped`. Stopped (hit a limit) is never called failed.
5. Cost and duration appear when the platform has them, rounded per `00-foundation.md`. Never omitted to look better; never dramatized.
6. Decisions explain *why* only when the why isn't obvious. "Chose `orders_eu` — region set to EU in step 1" is worth a line; "Called the model" is not.
7. Sources are cited as consulted, with locators. Never a source that wasn't opened.
8. Raw material — full prompts, JSON, tool payloads, token counts — lives inside the drill-in, never in the visible summary, unless the overlay is for a technical audience and says so.
9. When the agent acted on the user's behalf (sent, wrote, changed, deleted), that step is always expanded and states exactly what changed.
10. Never "I carefully considered…", "I made sure to…", "I double-checked…". Show the step, not the virtue.
11. When asked "why did you do X", answer with the decision line first, then the step list, not the other way round.

## Components

Step list / trace summary. Evidence for sources. Status strip on the reply. In surfaces with a canvas, selecting a step highlights the node.

## Examples

### Good — standard after-run
> 3 steps · 9s · $0.02 · all ran ok
> - `Extract fields` · ok · 4 fields extracted · 2.1s
> - `Check PO` · ok · matched `PO-88213` · 0.4s
> - `Route` · ok · → `AP-approve` · 6.4s
> 
> [each line opens to full input/output]

Why it works: skimmable in two seconds, auditable in two clicks.

### Good — failure expanded
> 3 steps · failed at step 2
> - `Extract fields` · ok · 4 fields extracted · 2.1s
> - **`Check PO` · failed** · `po_master` returned 503 after 3 retries (30.2s)
>   Input: `PO-88213` · Response: `503 Service Unavailable` · Retries: 3 × 10s
> - `Route` · skipped
> 
> [Retry from step 2] [Open the failing step]

Why it works: the failure is inline with its evidence; passing and skipped steps stay compact.

### Good — decision explained
> Used `contracts_2025.pdf` p.14 rather than the 2024 version — the question mentioned the September renewal, which only appears in 2025. [evidence]

Why it works: the choice was non-obvious; one line says what and why, with the source.

### Bad
> I began by carefully analyzing your request to determine the best approach. I then extracted the relevant fields from the invoice, making sure to double-check accuracy. Next, I verified the PO number against the master database. Finally, I routed the invoice appropriately. Everything completed successfully!

What's wrong: narrative instead of record, claims virtues instead of showing steps, no names, no numbers, no drill-in.

### Bad
> ```json
> {"steps":[{"id":"n1","type":"llm","model":"claude-sonnet","input":{"messages":[...]},"output":{...},"usage":{"prompt_tokens":1834,...
> ```

What's wrong: raw dump in the visible layer. This belongs inside the drill-in.

## Anti-patterns

- **The story** — steps as prose narrative.
- **The virtue signal** — "I carefully…", "I made sure…".
- **The JSON wall** — raw payloads in the summary.
- **The hidden pass** — collapsing so hard that passing steps can't be opened.
- **Stopped-as-failed** — reporting a max-turns stop as an error.
- **The invisible action** — an agent that sent an email and buried that fact in a collapsed step.

## Rubric

Checks `TR1`–`TRn` in `evals/rubrics.md` — the single source; rules here reference them, not the other way round.
