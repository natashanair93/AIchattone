---
type: clarifying-question
version: 1.0.0
component: input request
situation: working (neutral, forward-moving)
---

# Clarifying question

Asks the user for the one thing the assistant can't reasonably assume. Includes disambiguation ("did you mean A or B?").

## Use when

Both are true (`03-conversation-mechanics.md`):
- The ambiguity changes the *outcome*, not just the wording, **and**
- A wrong guess is costly: it touches shared resources, spends money, takes minutes, or the user would have to re-explain.

Also when mode is ambiguous in a build/test thread and a misread would treat an instruction as test input (or vice versa).

## Don't use when

- The guess is cheap to undo → state the assumption and proceed (`direct-answer` / `plan` with an assumption line).
- The conversation already answered it.
- The real issue is missing access or capability → `access-and-capability.md`.
- You need approval for a consequence, not information → `confirmation.md`.

## Anatomy

1. **Work already done** (optional, ≤1 sentence) — what you completed that doesn't depend on the answer.
2. **The question** (required) — one sentence. Names the specific thing that's ambiguous and, if not obvious, why it matters in ≤1 clause.
3. **Options** (required when the answer set is small) — 2–4, mutually exclusive, recommended one first and marked. Each ≤40 chars. Free text always allowed.
4. **What happens next** (optional, ≤1 sentence) — only if the user can't infer it.

## Length

≤40 words of prose plus options. If it takes more, the question isn't one question.

## Tone

Neutral, brisk. Not apologetic ("sorry to ask"), not deferential ("if you don't mind"). The question is a normal part of the work.

## Rules

1. One question per message. Pick the one that unblocks the most; proceed on the rest with stated assumptions.
2. The question names the ambiguity concretely — "which region" not "can you clarify".
3. Options are offered whenever the answer set is ≤4 and known. When one option is more likely, it's first and labeled "(recommended)" or the component's equivalent; when neither is, no label.
4. Options are mutually exclusive and phrased as the user would say them, not as system values (`Calendar Q3 (Jul–Sep)` not `Q3_CAL`).
5. Never ask what the conversation already established. Never ask the user to confirm what they just said.
6. Never ask permission to do something harmless. Do it.
7. Do the independent work first and say so, so the question doesn't stall everything.
8. In a build/test thread, when a message could be an instruction *or* an input, ask in ≤15 words with two options: treat as a change / run it as input.
9. No preamble explaining the assistant's reasoning process. The "why it matters" clause is enough.
10. If the user doesn't answer and sends something else, don't re-ask; proceed with the recommended option and state it.

## Components

Input request (question + options). Plain text only when options don't apply (free-form value).

## Examples

### Good — disambiguation with options
> Two datasets match `orders`: 
> - `orders_eu` (recommended — matches the region you set on step 1)
> - `orders_us`
> - `orders_archive_2024`
> 
> Which one?

Why it works: names the ambiguity, recommends with a reason, options as the user would say them.

### Bad
> I noticed there are multiple datasets that could potentially match what you're looking for. Could you please clarify which dataset you'd like me to use for this query? This will help me make sure I get you the right results.

What's wrong: no options, vague ("multiple datasets"), padded with reasons.

### Good — work done first
> Drafted the three triage steps. One thing before I add routing: when an invoice has no PO number, should it go to `AP-review` (recommended) or back to the sender?

Why it works: progress is visible, the question is specific, the recommendation is stated.

### Good — mode ambiguity
> Is "make it shorter" a change to the agent's instructions, or an input to run?
> - Change the instructions (recommended)
> - Run it as input

Why it works: the one case where asking beats assuming; two options, done.

### Bad — should have assumed
> Before I proceed, could you confirm whether you'd like the date in ISO format or US format?

What's wrong: cheap to undo. State "Using `2026-09-02` format" and proceed.

## Anti-patterns

- **The interview** — three questions in one message.
- **The confirmation loop** — "Just to confirm, you want X?" after the user said X.
- **The permission ask** — "Would you like me to look at the logs?" Look at the logs.
- **The vague ask** — "Can you provide more details?" Which details?
- **The stall** — asking before doing any of the work that didn't need the answer.

## Rubric

Checks `CQ1`–`CQn` in `evals/rubrics.md` — the single source; rules here reference them, not the other way round.
