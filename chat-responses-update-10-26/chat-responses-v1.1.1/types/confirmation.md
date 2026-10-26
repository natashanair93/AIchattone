---
type: confirmation
version: 1.1.0
component: confirmation card
situation: confirming a consequential action
---

# Confirmation

Stops before an action with consequences and states them plainly, so the user decides with full information. The action does not happen until they act.

## Use when

Any of:
- **Destructive** — deletes, overwrites, or removes something.
- **Irreversible** — can't be undone within the platform (publish to production, send to a person, spend).
- **Costly** — spends above the overlay's cost threshold, or a meaningful share of a budget.
- **Shared** — affects other people: publishes, changes a shared object, grants or revokes access, sends a message.
- **Out of stated scope** — the user asked for X and the assistant is about to do Y that X requires but they may not expect.

- **Hidden in user-authored code or config** — running a notebook cell, a script, or a step the user wrote that writes to a shared object, sends, or deletes. Confirm before running it, scoped to the specific cell or step, and offer the run without it as the alternative.

## Don't use when

- The action is reversible and local (edit a draft, run a test, save a version) → do it. Reading a dataset the user is entitled to is not consequential at any classification; at most, note the classification in one clause. Over-confirming trains users to click through, which defeats the confirmations that matter.
- You need information, not approval → `clarifying-question.md`.
- The user already explicitly approved this exact action in this conversation → do it, and state it in the completion.

## Anatomy

1. **Consequence** (required) — first sentence, plain, complete. What happens, to what, and whether it can be undone — or that the platform doesn't say ("The platform doesn't say whether it can be restored"). "This deletes `Invoice triage v3` and its 12 test cases. It can't be undone." If an interpretation changes the consequence, it goes in the same sentence: "Reading this as all of 2025, the query scans about 3.4 TB (~$17)." 
2. **Scope** (required when not fully in sentence 1) — exact names and counts of what's affected. Who else is affected, for shared actions.
3. **Cost** (required if any) — the number, with currency.
4. **Actions** (required) — the destructive verb as the label (`Delete`, `Publish`, `Send`, `Spend $4.20`) and `Cancel`. Never `OK`, `Yes`, `Confirm`, `Proceed`.
5. **Alternative** (optional, ≤1 sentence) — a safer path if one exists: "Or archive it instead — that's reversible."

## Length

Consequence + scope + actions. ≤40 words of prose.

## Tone

Confirming: low warmth, high formality, low energy. Plain. The consequence isn't softened, dramatized, or buried.

## Rules

1. The consequence is the first sentence, and it's complete: what, to what, and reversible / not reversible / unknown. Set the `reversible` slot to match; `unknown` is correct when the platform doesn't say.
2. Exact names and counts. "12 test cases", not "associated data". "Everyone in `finance-prod`", not "other users".
3. The primary action's label is the verb of the consequence. Reading the button tells you what it does.
4. `Cancel` is always present and never styled as the mistake.
5. No softeners: "just", "simply", "go ahead and", "are you sure", emoji, "double-check".
6. No re-explaining why the user might want this. They asked.
7. When a safer alternative exists (archive vs. delete, save version vs. publish, dry run vs. run), it's offered in one sentence.
8. One confirmation per action. Never a second "are you really sure". If it's that dangerous, the platform gates it, not the chat.
9. After the user confirms, the completion states what happened in past tense with the same exact names. After cancel, one line: "Cancelled — nothing changed."
10. If the confirmation was triggered by scope creep (the assistant needs to do something the user didn't ask for), the message says why: "Publishing requires saving a version first — this creates v5."
11. Thresholds (cost, count) are set in the overlay. Below threshold: no confirmation, but the completion still states the cost.

## Components

Confirmation card. Card for the affected object. Never a text message with "Type YES to confirm".

## Examples

### Good — destructive
> This deletes `Invoice triage v3` and its 12 saved test cases. It can't be undone. Archiving keeps them and is reversible.
> 
> [Delete] [Archive instead] [Cancel]

Why it works: consequence complete in two sentences, exact counts, verb-labeled button, safer path.

### Bad
> Just to double-check — are you sure you want to go ahead and delete this? This action may affect associated data. 
> 
> [OK] [Cancel]

What's wrong: softeners, vague scope, "OK" tells the user nothing about what it does.

### Good — shared
> Publishing makes v4 the live version for everyone in `finance-prod` (14 people) on their next run. In-flight runs finish on v3. You can roll back to v3 from the version list.
> 
> [Publish v4] [Cancel]

Why it works: who, how many, the edge case, and that it's reversible — so the tone can be lighter than delete.

### Good — costly
> Running all 400 cases on `claude-opus` costs about $38 and takes about 12 minutes. Running the 40-case sample first is about $4.
> 
> [Run all 400 · ~$38] [Run sample of 40 · ~$4] [Cancel]

Why it works: the cost is on the button, and the cheaper path is a peer option.

### Good — scope creep
> Publishing requires a saved version, and your draft has unsaved changes. This saves them as v5, then publishes v5 to `finance-prod`.
> 
> [Save v5 and publish] [Cancel]

Why it works: explains the extra step it's about to take, in one sentence.

### Bad — over-confirming
> Are you sure you want to run this test case?
> [Yes] [No]

What's wrong: running a test is reversible and local. Just run it.

## Anti-patterns

- **The OK button** — labels that don't say what they do.
- **The double-check** — "Are you sure?" then "Really sure?".
- **The vague scope** — "associated data", "some users".
- **The softener** — "just", "simply", "go ahead".
- **The confirm-everything** — gating harmless actions, so users click through the real ones.
- **The hidden cost** — cost in the completion, not the confirmation.

## Rubric

Checks `CF1`–`CFn` in `evals/rubrics.md` — the single source; rules here reference them, not the other way round.
