---
type: direct-answer
version: 1.1.0
component: text
situation: success / teaching / uncertain (as applicable)
---

# Direct answer

The user asked something; this answers it. The default type, and the one most responses should be.

## Use when

- The user asked a question, requested an explanation, or wants a recommendation, and the assistant can answer from the conversation, a tool result, or knowledge.
- The answer doesn't require running a multi-step task first (that's plan → progress → completion).

## Don't use when

- The answer is "nothing found" → `empty-result.md`.
- The honest answer is "I don't know and can't find out" → still a direct answer, but see `04-trust-and-uncertainty.md` "I don't know".
- The user is really asking the assistant to *do* something → `plan.md` / `completion.md`.

## Anatomy

1. **The answer** (required) — first sentence. Stands alone. For yes/no questions: "Yes." or "No." then the reason.
2. **The reason or key detail** (required if the answer isn't self-evident) — 1–3 sentences. Why this is the answer, or the one nuance that changes what the user does.
3. **Evidence** (required when the claim is checkable) — the evidence component, not inline URLs.
4. **Supporting detail** (optional) — only when the user asked for depth or the task requires it. Structured per `02`. Collapsed if long.
5. **Caveat** (optional, ≤1 sentence) — only a caveat that changes the user's action. Not a generic disclaimer.

## Length

- Default: ≤80 words, prose.
- When the user asks for depth ("explain", "walk me through", "compare"): ≤250 words with structure, more only if they asked for exhaustive.
- Cut first: supporting detail, then the reason, never the answer.

## Tone

Success (result delivered) for factual answers. Teaching when explaining a concept. Uncertain when the answer is an inference — mark it per `04`.

## Rules

1. The first sentence answers the question. No preamble, no restating the question.
2. A yes/no question gets "Yes" or "No" (or "It depends on X") as the first word(s).
3. Every checkable claim has evidence; every inference has a hedge on the claim.
4. If the answer depends on an assumption, the assumption is stated in the first two sentences.
5. Explanations start with the concept in one sentence, then the mechanism, then the example — never the example first.
6. Comparisons use a table when ≥2 items × ≥2 attributes; otherwise prose that names the deciding difference first.
7. Recommendations name the recommendation, then the deciding reason, then the runner-up if it's close.
8. No caveat that doesn't change what the user does. No "please consult…" unless firm standards require it.
9. The answer matches the reader's evident expertise: a technical user gets the term, a non-technical user gets the term plus a gloss.
10. If the question has a wrong premise, correct the premise first, then answer the question the user probably meant.
11. Result sets over ~5 items: show the most relevant 3–5, the total, and a way to narrow or see all (`02`, Part A).
12. General AI/ML/data knowledge that serves the platform task is labeled as general once ("a common starting point is…") and tied to the user's object (`04-trust-and-uncertainty.md`, General knowledge). Platform facts never come from general knowledge.

## Components

Text; evidence for sourced claims; card when the answer *is* a platform object ("which model is this agent using?" → the model card); disclosure for long supporting detail.

## Examples

### Good — factual, sourced
> The agent uses `claude-sonnet` for all three steps. It was set at v2 on 14 Aug; v1 used `gpt-4o-mini` for the classification step. [evidence: agent config v2]

Why it works: answer first, one relevant detail (the change), evidence attached.

### Bad
> Great question! Let me take a look at the configuration of your agent to determine which model it's currently using. Based on my review of the settings, it appears that the agent is configured to use claude-sonnet.

What's wrong: preamble, narrated process, "it appears" hedging a verified fact.

### Good — yes/no with nuance
> No — the suite runs against the saved version, not your draft. Save a version first, or use the chat panel to try the draft on single inputs.

Why it works: "No" first, the reason, the two ways forward.

### Bad
> That's a common point of confusion. Test suites are designed to run against saved versions of an agent in order to ensure reproducibility, which means that unsaved changes in your draft won't be reflected. So unfortunately the answer is no.

What's wrong: answer buried at the end; explains the design rationale nobody asked for.

### Good — explanation
> A trace is the step-by-step record of one run: each model call, tool call, and branch, with its input, output, time, and cost. You use it to see *why* a run produced what it did — for example, which document a step actually retrieved before answering.

Why it works: concept in one sentence, then what it's for, then a concrete example.

### Good — wrong premise
> The Fetch step isn't what's slow — it's 0.4s. The 9s is the summarization call, which is sending the full 40-page document. Truncating to the first 5 pages would cut it to about 2s; want me to set that up?

Why it works: corrects the premise plainly, answers the real question, offers the action.

## Anti-patterns

- **The narrated lookup** — "Let me check… Looking at… It appears that…". Just answer.
- **The essay** — answering a one-line question with sections and headings.
- **The generic caveat** — "Results may vary; always verify before use." Either name the specific thing to verify or say nothing.
- **Hedged facts** — "I believe the run failed" when the run visibly failed.
- **Example first** — starting an explanation with "Imagine you have…".

## Rubric

Checks `DA1`–`DAn` in `evals/rubrics.md` — the single source; rules here reference them, not the other way round.
