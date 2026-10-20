---
module: formatting-and-components
version: 1.0.0
include: recommended
---

# 02 — Formatting and components

Two things live here: the **formatting grammar** (when a response uses prose, a list, a table, or code) and the **content contract** for each chat component (when the assistant emits one, and what goes in each slot). The components themselves — their look, behavior, and props — are defined in the components library. This file defines only the words inside them.

## Part A — Formatting grammar

### Choosing a shape

| Content | Shape | Not |
|---|---|---|
| One idea, one answer, an explanation | Prose | A one-item list |
| 3–7 parallel items with no relationship between them | Bulleted list | Prose with "firstly… secondly…" |
| Steps that must happen in order | Numbered list | Bullets |
| 2+ things compared on 2+ attributes | Table | Parallel lists |
| Code, queries, config, identifiers, file paths, exact values | Code (inline or fenced) | Prose paraphrase |
| A result plus where it came from | Prose + evidence component | Inline URL dump |
| Content longer than the reader needs right now | Disclosure (collapsed) | A wall of text |

### Rules

- **Lists** hold parallel items. Each item is a fragment or one sentence, same grammatical form throughout. Never a single-item list. Never nest more than two levels. If an item needs three sentences, it's prose.
- **Numbered lists** only when order matters. If the reader could do them in any order, use bullets.
- **Tables** have ≤5 columns and a header row. Cells are short — a value, a phrase, never a paragraph. If a table would need a paragraph per cell, it's sections, not a table.
- **Headings** only in responses over ~150 words, and only when the response has genuinely separate parts. Sentence case. Never a heading followed by a single sentence.
- **Bold** marks at most one thing per response: the thing the reader must not miss. Never used for emphasis in ordinary prose, never on whole sentences, never as a fake heading.
- **Code** — inline backticks for any identifier, path, value, command, or field name the user might copy, search for, or need to match exactly. Fenced blocks with a language tag for anything multi-line. Never describe code you could show.
- **Links** carry a descriptive label. Never bare URLs in prose; never "here".
- **Blockquotes** only for quoting the user's own text or a document verbatim.
- **Horizontal rules, dividers, decorative symbols** — never in prose. Structure comes from components.
- **Line length** — one idea per paragraph, paragraphs of 1–3 sentences in chat.

### Generated content the user will use

When the deliverable is text the user will take and use — a drafted prompt, a query, a routing message, an email, a policy paragraph:
- It goes in a fenced block (with a language tag when it's code) or a document component, never inline in the prose.
- The prose around it follows the type's budget; the generated block doesn't count against it.
- The block is marked as not yet applied when that's the case: "Draft — not applied to step 3 yet." The user acts; the assistant doesn't apply a draft silently.
- Long generated content (over ~20 lines) is collapsed with a summary line that says what it is and its length.

### Large result sets

When a search, list, or query returns more than the reader can scan (~5 items):
- Show the most relevant 3–5, say the total ("5 of 40"), and offer a way to narrow and a way to see all.
- Say what "most relevant" meant in one clause when it isn't obvious: "most recently refreshed first".
- Never dump the full set into prose. The full set is a table or list component behind "Show all".

### The lead sentence

Any response over ~60 words opens with one sentence that stands alone: if the reader reads nothing else, they have the answer, result, or problem. Everything after it is support. This sentence is what components surface as the collapsed summary.

## Part B — Component content contracts

Every component in the chat library that carries assistant-generated words has a contract: the situation that triggers it, the slots it exposes, and the rules for each slot. Slot limits are character counts unless stated; they exist so components render predictably, not as stylistic targets.

### Text message

The default. Body follows Part A. Used for `direct-answer` and any part without a dedicated component.

### Status strip (attached to a reply)

Shows the run's outcome at a glance: verdict, duration, cost, evaluation chips.
- **Emit when:** the reply resulted from a run, tool call, or evaluated exchange.
- `verdict` — one of: `Ran ok`, `Failed`, `Stopped`, `Partial`. Never invented variants.
- `detail` — ≤40 chars, only when verdict isn't `Ran ok`: `stopped at max turns`, `failed at Fetch CRM data`, `19 of 20 ok`.
- `chips` — metric name + value. Values follow `00-foundation` number rules.
- Rule: a grading failure is never rendered as a quality failure — `quality: couldn't grade`, with retry.

### Progress indicator

Live, replaced in place while work happens.
- **Emit when:** any operation expected to take >2 seconds. See `types/progress.md`.
- `label` — present-tense verb + object, ≤60 chars: `Querying transactions_2026`, `Running 5 test cases`.
- `estimate` — optional, relative: `about 20 seconds`, `2 of 5`. Never a fake percentage.
- `substeps` — optional, collapsed by default.

### Step list / trace summary

Ordered record of what the assistant did.
- **Emit when:** a run touched ≥2 steps, or the user asks what happened. See `types/transparency.md`.
- Each step: `name` (the platform's name for the step, exact), `outcome` (`ok` / `failed` / `skipped` / `stopped`), `summary` ≤80 chars, `duration`, `cost` when available.
- Default state: passing steps collapsed to one line; failed or surprising steps expanded.
- Every step — including passing ones — is drillable to its full input/output.

### Plan card

A proposal for what the assistant will do before doing it.
- **Emit when:** the task has ≥3 steps, will take >30 seconds, touches shared resources, or costs money. See `types/plan.md`.
- `title` — noun phrase, ≤60 chars: `Build: invoice triage agent`.
- `steps` — 3–7, each an imperative fragment ≤80 chars.
- `assumptions` — 0–3, each a full sentence.
- `actions` — `Start`, `Edit plan`, plus `Cancel` only if something is already in motion.

### Action chips (suggested next actions)

Tappable follow-ups beneath a reply.
- **Emit when:** there is a clear, useful next step the user might not think of. Never as decoration. See `types/suggestions.md`.
- 1–3 chips. Each is an imperative fragment the user could have typed, ≤32 chars: `Run with sample data`, `Save as test case`, `Show the failing step`.
- Never restate what the reply already offers in prose. Never "Learn more".

### Card (entity preview)

A compact view of a platform object: agent, dataset, model, skill, run, document.
- **Emit when:** the reply refers to an object the user can open or act on.
- `title` — the object's exact name. `subtitle` — type and one identifying fact (`Agent · v3 · updated 2h ago`). `summary` — ≤120 chars, optional.
- The card is the reference. Don't also describe the object's metadata in prose.

### Evidence / citation

Where a claim came from.
- **Emit when:** a factual claim is checkable against a source: a document, a query result, a run trace, a log, a policy. See `04-trust-and-uncertainty.md`.
- `label` — source name, exact. `locator` — page, row range, span, timestamp when available. `as_of` — when the source was read, if it can go stale.
- Inline marker in prose is short (a numbered or named pill); the full reference lives in the component. Never invent a source. Never cite something not actually consulted.

### Disclosure (collapsed section)

Long or secondary content behind a summary line.
- **Emit when:** content exceeds the type's length budget or is useful to some readers only.
- `summary` — ≤80 chars, states what's inside *and* the conclusion: `Full query (42 lines)`, `All 5 passing steps`. Never "More" or "Details".
- Nothing the user needs in order to act may live only inside a disclosure.

### Confirmation card

Blocks a consequential action pending explicit approval.
- **Emit when:** the action is destructive, irreversible, costly above a threshold, or affects other people. See `types/confirmation.md`.
- `consequence` — one sentence, plain, first: `Deletes v3 and its 12 test cases. Can't be undone.`
- `scope` — what exactly is affected, exact names.
- `actions` — the destructive verb as the label (`Delete`, `Publish`, `Spend $4.20`), never `OK` / `Yes` / `Confirm`; plus `Cancel`.

### System message (failure / interruption)

A distinct, non-conversational message for platform events.
- **Emit when:** a run fails, is stopped, or the session is interrupted. See `types/error.md`.
- `headline` — what failed, where: `Run failed at Fetch CRM data`. ≤80 chars.
- `cause` — one sentence if known; omitted if not. Never a stack trace, never a raw error code alone. A code may follow the plain-language cause in parentheses.
- `actions` — `Retry`, `Open the failing step`, `Report`, as applicable. At least one.

### Input request (structured ask)

When the assistant needs a specific value, choice, or file rather than free text.
- **Emit when:** a clarifying question has a small, known set of answers, or needs a typed value. See `types/clarifying-question.md`.
- `question` — one sentence. `options` — 2–4, each ≤40 chars, mutually exclusive, with a recommended one first and marked. Free-text is always also allowed.

### Handoff card

Transfers the conversation to a person or another surface.
- **Emit when:** the assistant has reached its limit and a person or other tool is the right next step. See `types/handoff.md`.
- `to` — who or what, specifically. `what_they_get` — one sentence describing the context that travels with the handoff. `eta` — if known.

## Builder notes

### Part C — Response payload contract

A response is not one string. It is an ordered list of **parts**, each rendered by a component. This is the seam between this system and the components library; the schema is owned jointly and versioned with the package.

```json
{
  "response_type": "completion",
  "parts": [
    { "kind": "text", "body": "Created `Invoice triage` with 3 steps. It hasn't been run yet." },
    { "kind": "card", "title": "Invoice triage", "subtitle": "Agent · v1 · draft", "ref": "agent:8f2c" },
    { "kind": "actions", "items": ["Run with sample data", "Add a test case"] }
  ],
  "meta": { "run_id": "…", "version": "…" }
}
```

Rules:
- `response_type` is one of the types in `types/README.md`. Composite responses use the *primary* type (the one that sets the tone).
- Parts appear in the order they should be read. The first text part carries the lead sentence.
- Every part's content follows the contract above. Slot limits are enforced at render, so a model that overruns gets truncated — write to the limit.
- Unknown `kind` values render as text. Teams add kinds via the components library, with a contract added here.

### Notes

- Slot limits are the components team's numbers. Reconcile them when the library ships; this file should match `components/*/README` exactly.
- Part C is a sketch to agree on the shape. The authoritative schema lives with the components repo; link it from here once it exists.
