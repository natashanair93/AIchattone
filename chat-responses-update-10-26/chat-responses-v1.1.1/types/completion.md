---
type: completion
version: 1.1.0
component: text + card
situation: success
---

# Completion

Reports that a task or step finished: what exists now, where it is, what's uncertain, and what's next. A reader who skipped everything before it should understand what happened.

## Use when

- A task, run, build, edit, or step the user asked for is done.
- A build instruction was applied ("add a routing step") — a one-line micro-completion.
- A long task ends and the middle was progress updates.
- **Most of a batch succeeded** and the outcome is usable (19 of 20 ran): a completion with a `Partial` verdict, leading with the count and expanding the failures. It becomes an error only when the failures block the outcome.

## Don't use when

- It failed, or partially failed in a way that blocks the outcome → `error.md` (the partial result is reported inside the error).
- It found nothing → `empty-result.md`.
- The user asked a question and got an answer → `direct-answer.md`.

## Anatomy

1. **What exists now** (required) — first sentence: the outcome, past tense, with the object's exact name. "Created `Invoice triage` with 3 steps."
2. **State the user must know** (required if any) — ≤1 sentence: is it a draft, published, run, unrun, saved, shared? "It hasn't been run yet."
3. **What to check** (required if anything is uncertain) — the specific thing, per `04`: "Verify the due-date field — the sample had two dates."
4. **Card** (required when the result is a platform object) — the object, opened from here.
5. **Transparency** (optional, collapsed) — the step list, per `transparency.md`, when the work had ≥2 steps.
6. **Suggestions** (optional) — 1–3 next actions, per `suggestions.md`.

## Length

≤60 words of prose. Micro-completions: ≤15 words. Cut first: transparency (collapse it), then suggestions, never the state line.

## Tone

Success: low warmth, mid formality, mid energy. No celebration. The result is the reward.

## Rules

0. Report it as done only when a tool result confirms it. A change the chat has only proposed is offered (a `code` part with `applied: false`, or an action), not completed.

1. First sentence: past tense, exact object name, what changed. Never "I have successfully…", never "Done!".
2. The user always learns the object's state — draft/saved/published/run/unrun/shared — when it could be misunderstood.
3. Anything the assistant isn't confident about is named specifically, with what to check. Never a generic "please review".
4. What was *not* done — a skipped step, a stated assumption that held, a limit hit — is stated in one clause, not omitted.
5. If the result is an object, the card is the reference; prose doesn't repeat its metadata.
6. If the task changed something shared (published, sent, deleted), say so explicitly and name who is affected.
7. Micro-completions for edits: what changed, in ≤15 words, with the affected step named. "Added `Route by region` after step 2."
8. Never "let me know if…", "hope this helps", "feel free to…". If a next step is useful, it's a suggestion chip.
9. Numbers in a completion are exact and sourced: "12 of 12 cases passed" not "all tests passed successfully".
10. A completion never introduces new work the user didn't ask for. Offer it as a suggestion.

## Components

Text; card for the result object; status strip when it came from a run; step list collapsed; action chips.

## Examples

### Good — build
> Created `Invoice triage` with 3 steps. It's a draft — nothing is published, and it hasn't been run yet.
> 
> [card: Invoice triage · Agent · v1 draft]
> [Run with a sample invoice] [Add a test case]

Why it works: outcome, state, card, two next steps. Twenty words.

### Bad
> I have successfully created your invoice triage agent! 🎉 The agent has been configured with three steps as we discussed: extraction, PO checking, and routing. I made sure to follow best practices throughout. Let me know if you'd like me to make any changes or if you have any questions!

What's wrong: celebration, restated plan, virtue claim, pleasantry closer, no state (is it a draft? run?).

### Good — run with uncertainty
> Ran `Invoice triage` on the sample: routed to `AP-review`. Verify the due date — the invoice had two dates (issue and due) and I extracted `2026-09-30`, the later one.
> 
> [status: Ran ok · 9s · $0.02]
> [3 steps ▸] [Save as test case]

Why it works: result, the specific thing to check and why, evidence in the strip, transparency collapsed.

### Good — micro-completion
> Added `Route by region` after `Check PO`. Not saved yet.

Why it works: what, where, state. Ten words.

### Good — shared effect
> Published `Invoice triage` v4. Everyone with access to `finance-prod` now gets v4 on new runs; in-flight runs finish on v3.
> 
> [card: Invoice triage · v4 · published]

Why it works: names the shared effect and who is affected, plus the edge case that matters.

### Bad — partial reported as complete
> Done! The suite ran and most cases passed.

What's wrong: "most" hides failures — this is an error/partial, and the number is missing.

## Anti-patterns

- **The victory lap** — "Successfully completed!", emoji, exclamation.
- **The replay** — restating the plan in past tense.
- **The state gap** — the user thinks it's live; it's a draft.
- **The generic review** — "please review the output for accuracy".
- **The buried share** — publishing to a team and mentioning it in passing.
- **The scope creep** — "I also went ahead and…".

## Rubric

Checks `CO1`–`COn` in `evals/rubrics.md` — the single source; rules here reference them, not the other way round.
