---
type: progress
version: 1.0.0
component: progress indicator
situation: working
---

# Progress

Tells the user what is happening right now while work is in flight, so waiting feels like watching rather than wondering.

## Use when

- Any operation expected to take more than ~2 seconds.
- Any multi-step task, at each meaningful boundary.
- Streaming output that will take more than a few seconds to complete.

## Don't use when

- The work is instant — just show the result.
- The work finished — `completion.md`.
- The work failed — `error.md`. A progress update never reports a failure; it is replaced by the error.

## Anatomy

1. **Label** (required) — present-tense verb + exact object, ≤60 chars. "Querying `transactions_2026`". "Running case 3 of 12".
2. **Estimate** (optional) — relative and honest: "about 20 seconds", "2 of 5 steps", "usually under a minute". Never a made-up percentage.
3. **Sub-steps** (optional, collapsed) — for multi-step work, the step list with the current step marked.
4. **Interim result** (optional) — when a partial result is useful before the whole finishes: "3 of 12 passed so far".

## Length

One line per update. Updates replace each other in place; they don't stack into a log. The final state is replaced by a completion or error.

## Tone

Working: still, brisk, no warmth. No apology for time. No filler.

## Rules

1. The label says what is being done to what, in the platform's terms, present tense.
2. Update at meaningful boundaries — a step starts or ends, an estimate changes, a partial result lands — not on a timer.
3. Estimates are honest: if unknown, say "usually under a minute" or nothing; never fabricate a percentage or countdown.
4. When an estimate is exceeded by more than ~2×, say so and what's happening: "Taking longer than usual — the CRM API is slow to respond. Still waiting; I'll stop at 60s."
5. Long operations have a stated stop point (timeout, max turns, budget) that the user can see before it's hit.
6. Streaming text shows as it arrives; the assistant never fakes streaming with a spinner and then dumps a block.
7. The user can interrupt at any point; see `03-conversation-mechanics.md`. Progress messages don't need to say "you can stop me" every time — once per task at most.
8. Never "please wait", "hang tight", "bear with me", "processing your request", "almost there".
9. Never narrate the assistant's thinking as progress ("Thinking about the best approach…"). Progress is about *work*, not deliberation. If the platform shows reasoning, it's a separate, collapsed component.
10. When the work includes calling a tool the user might not expect (their calendar, an external API, a paid model), the label names it, so the transparency is live, not retrospective.

## Components

Progress indicator; step list (collapsed, current step marked) for multi-step work; status strip once done. In surfaces that show live traces, the progress label is the same text as the step name in the trace.

## Examples

### Good
> Querying `transactions_2026` · about 20 seconds

### Good — multi-step
> Running suite `Invoice regression` · case 7 of 40 · 6 passed, 1 failed so far

Why it works: what, where in the sequence, and a useful interim result.

### Good — exceeded estimate
> Still waiting on `Fetch CRM data` — 45s, usually 3s. The CRM API is slow. I'll stop at 60s and retry once.

Why it works: honest, names the cause if known, states the stop point.

### Bad
> Please wait while I process your request… This might take a moment. Thank you for your patience!

What's wrong: says nothing about what's happening; apologizes for time; pleasantry.

### Bad
> Thinking about the best way to approach this… Analyzing the problem… Formulating a plan…

What's wrong: narrates deliberation, not work. Nothing here is checkable.

### Bad
> 73% complete

What's wrong: fabricated precision — unless the platform really knows it's 73%, this is a lie.

## Anti-patterns

- **The spinner with a sentence** — "Working on it…" with no object.
- **The timer log** — a new message every 5 seconds saying the same thing.
- **The fake percentage** — progress bars that don't measure anything.
- **The silent overrun** — the estimate said 20s, it's been 2 minutes, nothing changed on screen.
- **The narrated brain** — "Let me think…", "Considering options…".

## Rubric

Checks `PR1`–`PRn` in `evals/rubrics.md` — the single source; rules here reference them, not the other way round.
