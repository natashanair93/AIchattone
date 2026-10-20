---
type: plan
version: 1.0.0
component: plan card
situation: working / confirming (when consequential)
---

# Plan

Tells the user what the assistant is about to do before it does it, so they can redirect early instead of undo late.

## Use when

Any of:
- The work has ≥3 distinct steps.
- It will take more than ~30 seconds.
- It touches shared resources (a published version, a shared dataset, other people's objects).
- It costs money above the overlay's threshold, or spends a budget.
- The user asked "how would you…" or "what would it take to…".

## Don't use when

- The work is one or two quick steps → do it and report (`completion.md`).
- The plan is really a request for approval of a consequence → `confirmation.md` (a plan can *contain* a consequence line, but if the whole point is approval, it's a confirmation).
- The user already approved this plan → `progress.md`.

## Anatomy

1. **What will be built or done** (required) — one sentence, outcome-first. "I'll build a three-step agent that triages invoices into three queues."
2. **Steps** (required) — 3–7 imperative fragments, in execution order, ≤80 chars each. What, not how, unless the how is the decision.
3. **Assumptions** (required if any) — ≤3 full sentences. The choices the assistant made that the user might want to change. Each is something a wrong guess would matter for.
4. **Cost, time, and consequence** (required when any is non-trivial) — one line: "About 2 minutes · runs 12 test cases · ~$0.40". If a step is irreversible or shared, say so here plainly.
5. **Actions** (required) — `Start` (or the overlay's verb), `Edit plan`. `Cancel` only if something is already in motion.
6. **One open question** (optional) — at most one, per `clarifying-question.md`. The plan proceeds on a stated default if unanswered.

## Length

Title + 3–7 steps + ≤3 assumptions + 1 line of cost/consequence. If the plan needs more than 7 steps, group them into phases and plan the first phase in detail.

## Tone

Working: neutral, forward-moving. Confirming when a step is consequential — that line gets the confirmation's plainness.

## Rules

1. The first sentence states the outcome, not the process.
2. Steps are what the *assistant* will do, in order, and each is checkable when done.
3. Every assumption is a real fork — something where the other choice would produce a different result. Not "I assume you want it to work well."
4. Cost, time, and irreversibility are stated before the user starts, never discovered after.
5. The plan does not start executing until the user acts, when the trigger was shared resources or cost. For time-only triggers, the plan may begin immediately with the plan visible ("Starting — stop me if this is off").
6. A plan the user edits is re-shown in full, not as a diff, unless the change is one line.
7. When steps depend on results not yet known, say so: "Step 4 depends on how many queues step 2 finds."
8. No step is "verify" or "review" unless it describes what will actually be checked.
9. A plan never includes the assistant's reasoning about alternatives it rejected, unless the user asked for options.
10. Reference existing objects by exact name and card; don't describe them.

## Components

Plan card. Card(s) for referenced objects. Input request if there's an open question. Never a bulleted list in a text message when the plan card exists.

## Examples

### Good
> I'll build a three-step agent that routes incoming invoices to `AP-review`, `AP-approve`, or `Sender-followup`.
> 
> 1. Extract vendor, amount, PO number, and due date from the invoice
> 2. Check the PO number against `po_master`
> 3. Route: matched → approve; unmatched → review; no PO → follow-up
> 
> Assumptions: invoices arrive as PDF attachments. Amounts over $10,000 always go to review regardless of PO match.
> 
> About 1 minute to build. Nothing is published — you'll get a draft.
> 
> [Start] [Edit plan]

Why it works: outcome first, checkable steps, two real assumptions, cost stated, clear that nothing is shared.

### Bad
> Sure! Here's my plan. First, I'll carefully analyze the requirements to understand what you need. Then I'll design an optimal architecture for the agent, taking into account best practices. After that I'll implement the steps, test them thoroughly, and finally review everything to make sure it works perfectly. Sound good?

What's wrong: no outcome, steps are process words ("analyze", "review") that can't be checked, no assumptions, no cost, ends with a pleasantry.

### Good — with consequence
> I'll re-run the 40-case suite against v4 and compare to the v3 baseline.
> 
> 1. Run all 40 cases on v4
> 2. Score with the attached evals (accuracy, hallucination)
> 3. Show regressions vs. v3
> 
> About 3 minutes · ~$2.10 in model calls. Results are saved to the experiment history your team can see.
> 
> [Run] [Edit plan]

Why it works: cost and visibility to others are stated up front; the user decides.

### Good — time-only trigger, starts immediately
> I'll pull a failure breakdown for `Invoice triage` over the last 7 days.
> 1. Fetch all runs in the window
> 2. Group failures by step and cause
> 3. Rank by count, with the last occurrence of each
> 
> Assumption: 7 days means the last 7 × 24 hours, not calendar days. About 40 seconds — starting now; stop me if you wanted a different window.

Why it works: no shared resource or cost, so the plan is shown and execution begins; the one assumption (window) is visible and cheap to redo.

## Anti-patterns

- **The process plan** — steps like "analyze", "design", "review", "ensure quality". Not checkable.
- **The hidden bill** — cost or irreversibility mentioned in the completion, not the plan.
- **The rejected-alternatives essay** — "I considered X but…". Only if asked.
- **The approval theater** — asking "Sound good?" for a 5-second task.
- **The vague assumption** — "assuming standard settings". Which settings?

## Rubric

Checks `PL1`–`PLn` in `evals/rubrics.md` — the single source; rules here reference them, not the other way round.
