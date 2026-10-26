---
type: error
version: 1.1.0
component: system message (platform) / text (user-input)
situation: system failure / user made a mistake / uncertain
---

# Error

Something failed. Names what, where, and what to do — in that order, in two or three sentences.

Three sources, three slightly different shapes:
- **User-input error** — the user gave something malformed, missing, or contradictory.
- **Platform error** — a run, tool, API, or the platform itself failed.
- **Model-quality error** — the assistant produced something wrong and is correcting it, or can't produce a usable result.

## Use when

- A run, step, tool call, query, build, or action failed or stopped abnormally.
- The user's input can't be used as given.
- The assistant realizes a previous answer was wrong.
- A partial result exists *and the failure blocks the outcome* — this is an error that carries the partial. When most of a batch succeeded and the result is usable, it's a `completion.md` with a `Partial` verdict instead.

## Don't use when

- A guardrail blocked it → `guardrail.md`.
- The user lacks access, or the capability doesn't exist → `access-and-capability.md`.
- A search found nothing (that's not a failure) → `empty-result.md`.
- It hit a stated limit (max turns, budget) and that's expected behavior → still an error-shaped message, but the outcome is `stopped` and the tone is neutral.

## Anatomy

1. **What failed, where** (required) — first sentence. The exact step, object, or field. "The run failed at `Check PO`." "The date in step 1 isn't in a format I can read."
2. **Cause** (required if known, ≤1 sentence) — plain language. A code may follow in parentheses. If unknown, say so: "I don't know why yet — the API returned no message."
3. **What to do** (required) — ≥1 concrete action as a button or chip: `Retry`, `Open the failing step`, `Use 2026-09-02 format`, `Report this`. For user-input errors, the fix is often offered as a one-click option with the assistant's best guess.
4. **Partial result** (required if any) — what did complete and whether it's usable. "Steps 1–2 completed; their output is saved."
5. **Transparency** (optional) — failing step expanded, per `transparency.md`.

## Length

≤3 sentences of prose + actions. A `code` part with the fix doesn't count (2 is the norm; the third is for a partial result or a cross-workspace fact that changes the fix). The cause is never a paragraph; the paragraph lives in the drill-in.

## Tone

- Platform error: mid warmth, brisk. One short apology allowed if the platform caused it, in the same sentence as the next action.
- User-input error: mid warmth, no blame. State what's needed, not what they did wrong.
- Model-quality error: neutral, direct. "That was wrong — X, not Y." No groveling.
- Stopped at a limit: neutral. It's not a failure.

## Rules

1. Name the thing. Never "an error occurred", "something went wrong", "unable to process", "invalid input".
2. Active voice. "The CRM API returned a 503" not "an error was encountered".
3. Cause in plain language first; the code, if any, after it in parentheses. Never a code alone. Never a stack trace in the visible layer.
4. At least one action, and the first action is the most likely fix.
5. User-input errors state the requirement and, where possible, offer the assistant's best-guess correction as a one-click option. Never "invalid", never "you entered".
6. Partial results are reported and their usability is stated. Never silently discarded.
7. On repeated failure (same step, same cause, 2×), the message changes approach: names that retrying won't help and proposes something different. Never a third identical retry.
8. Stopped-at-limit uses the word "stopped", names the limit, and offers to raise it or continue — unless continuing can't help (a loop with nothing to find), in which case say so and offer the fix instead: "Stopped at 10 turns (the max). Continue for 10 more, or open the run." Quotas and rate limits follow the same shape: name the limit, say when it resets or who can raise it: "Stopped — `finance-prod` has used its daily model budget ($200). It resets at 00:00 ET; the workspace owner can raise it."
9. When the assistant corrects itself, the correction is first, the retraction second, and there is no apology beyond one clause: "Correction: the step is 4% of cost, not 40%. I misread the table."
10. Never blame the user, the model, a vendor, or "the system". Name what happened.
11. Never promise it won't happen again. Never "please try again later" without a specific reason and time.
12. The `Report` action exists for platform errors the user can't fix; it carries the run ID so they don't have to.
13. When the user is frustrated, the acknowledgement is folded into the first sentence (≤1 clause) alongside what failed — never a separate sentence before it (`03-conversation-mechanics.md`, Frustration).

## Components

System message for platform errors and stops. Text with input request or action chips for user-input errors. Step list with the failing step expanded. Status strip shows `Failed` or `Stopped` with the step name.

## Examples

### Good — platform
> The run failed at `Check PO` — `po_master` returned a 503 after three retries. Steps 1–2 completed and their output is saved.
> 
> [Retry from step 2] [Open the failing step] [Report]

Why it works: what, where, cause, partial, actions. Two sentences.

### Bad
> Oops! Something went wrong while processing your request. Please try again later or contact support if the problem persists. Error code: ERR_UPSTREAM_503.

What's wrong: names nothing, blames nothing, the code is the only fact and it's last; "try again later" with no reason.

### Good — user input
> I need the date as `2026-09-02`. I read `09/02/26` as 2 September 2026 —
> [Use 2 Sep 2026] [Use 9 Feb 2026] [Type a date]

Why it works: requirement stated, best guess offered as one click, no "invalid".

### Bad
> Invalid date format. You entered "09/02/26". Dates must be in ISO 8601 format (YYYY-MM-DD).

What's wrong: "invalid", "you entered", spec name instead of an example, no offer to fix it.

### Good — stopped at limit
> Stopped at 10 turns (the max for this agent) without reaching a final answer. The last step was `Search knowledge` for the third time — it may be looping.
> 
> [Continue for 10 more turns] [Open the run]

Why it works: "stopped" not "failed", the limit named, a useful observation, two paths.

### Good — repeated failure
> Third 503 from `po_master` on the same step, so retrying won't help. Options: raise the timeout to 60s, or route unmatched invoices to review while the API is down.
> 
> [Raise timeout and rerun] [Route to review for now]

Why it works: acknowledges the pattern in one clause, changes approach, two concrete paths.

### Good — self-correction
> Correction: `Fetch CRM data` is 71% of cost, not 7% — I dropped a digit. The recommendation stands: that's the step to optimize.

Why it works: correction first, cause in one clause, what still holds.

## Anti-patterns

- **The oops** — "Oops", "Uh-oh", "Something went wrong".
- **The passive** — "an error was encountered", "the request could not be processed".
- **The code-only** — `ERR_42` and nothing else.
- **The blame** — "you entered an invalid…", "the vendor's API is unreliable".
- **The infinite retry** — same action, three times, same result.
- **The lost partial** — 9 of 10 steps ran and the message says only "failed".
- **The grovel** — "I sincerely apologize for the inconvenience this has caused."
- **Failed-for-stopped** — reporting a max-turns stop as a failure.

## Rubric

Checks `ER1`–`ERn` in `evals/rubrics.md` — the single source; rules here reference them, not the other way round.
