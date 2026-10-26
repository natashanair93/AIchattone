# Evaluating responses against the system

v1.1 adds `framework.md` (quality scores, failure attribution, coverage, release gates) and `judge-prompt.md` (the judge for both). The per-response compliance method below is unchanged and is Layer 1 of the framework.

A rule that can't be checked is a suggestion. This folder makes the system checkable: a universal rubric every response is graded on, a per-type rubric for its type, and a method for running them against real transcripts.

## What gets graded

A **response** — one assistant turn, with its parts — in the context of the conversation before it. The grader sees the conversation up to and including the response, the overlay in use, and the rubrics. It does not see the system prompt (the point is to grade the output, not the input).

Each response is graded on:
1. **Type selection** — was this the right type for the situation? (`types/README.md` "Choosing the type")
2. **Universal rubric** — the checks every response must pass.
3. **Type rubric** — the checks for its type.
4. **Overlay rules** — the domain rules' rubric lines.

Every check is binary. A response's score is the fraction of checks passed; a response *fails* if it fails any check marked **blocking** in `rubrics.md`.

## How to run it

Two tiers, so the check that gets run is the one that matters.

**Smoke (every change to a team prompt or overlay).** 5 real transcripts — at least one with a failure, one with a guardrail or access limit — graded on the **blocking** checks only, by the model judge below. Any blocking failure blocks the change. Ten minutes.

**Full (first release, and every package version bump).** 20 real transcripts, stratified so every type the chat uses appears at least twice and at least three transcripts contain a failure, guardrail, or access limit. All checks. Graded by people the first time (two graders, disagreements discussed); by the model judge after that, once its agreement with the human set is ≥85%. Ships when: no blocking failures; ≥90% of universal checks pass; ≥85% of type checks pass; type selection correct in ≥90% of responses. Below that, fix the prompt or the overlay — not the rubric.

Keep the transcripts. They're the calibration set for the judge and the regression set for the next bump.

## Judge prompt

```
You are grading one assistant response in a chat conversation against a content standard.

You will receive:
- The conversation up to and including the response to grade.
- The overlay in use (domain).
- The rubric: type-selection guide, universal checks, per-type checks, overlay checks.

Steps:
1. Decide which response type the situation called for, using the type-selection guide. State it.
2. Decide which type the response actually is. State it. If they differ, mark type-selection FAIL and explain in one sentence.
3. For each universal check, answer PASS or FAIL with a ≤15-word reason. Quote the offending text for FAILs.
4. For each check of the response's actual type, do the same.
5. For each overlay check that applies, do the same.
6. Output: a JSON object {type_expected, type_actual, checks: [{id, result, reason, quote}], blocking_failures: [ids]}.

Grade the response, not the conversation. Do not reward length, effort, friendliness, or thoroughness — only the checks. A short response that passes every check outscores a long one that fails one.
```

## Reading results

- **Many type-selection failures** → the prompt's "choosing the type" logic isn't landing; usually the team prompt is overriding it with task instructions. Check the team prompt for restated rules.
- **Universal failures clustered on openers/closers** → the most common first-release finding; fix by adding the overlay's own bad examples.
- **Type failures on error / guardrail / access** → the situation is rare in the transcripts, so the model has few examples; add domain examples to the overlay.
- **Overlay rule failures** → the rule may be untestable as written. Rewrite the rubric line, then the rule.

## Adding a check

Every new rule in any module ships with its rubric line here. The line must be binary and answerable from the response and conversation alone. "Is the response helpful?" is not a check. "Does the first sentence answer the question?" is.
