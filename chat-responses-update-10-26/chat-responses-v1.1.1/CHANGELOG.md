# Changelog

## 1.1.1 — 2026-10-26

Post-retest contract fixes and alignment with the Fusion Chat pattern library inventory. Not breaking for content; breaking for renderers that already parse 1.1.0 JSON.

- `02` Part B now lists every enum and object shape the model must emit: `card.object_type` values, button objects {`label`, `role`} (was an unnamed `kind`, which models renamed to `role` on their own in 7 of 72 responses), `status.metrics` {`label`, `value`}, `starters.items` {`label`}, `actions.items` {`label`, `intent`}.
- New part kind `candidates` (maps to Answer comparison cards); `code.variant: diff` (maps to Code diff view).
- `actions.intent`: `prompt` (suggested follow-up pill) vs. `action` (persistent button). Action chips must not auto-dismiss and must show on errors.
- `03`: "Modes in one thread" renamed "Change vs. input in one thread" (the pattern library's mode is Chat / Code / Spec). Slash commands and Test Mode count as explicit intent.
- `components/chat-components.md` v0.2: rewritten in the pattern library's five-field format, with slots, a mapping to library components, and ten decisions for the design system owner.
- `components/response.schema.json` v0.2 to match.

Retest of 1.1.0 (see the review page): holdout set (18 scenarios written independently) — 17/18 strong, 18/18 small, vs. 15/18 for 1.0.0 strong. Original set — 36/36 strong vs. 25/36 for 1.0.0. Schema conformance at 1.1.0: 100% valid JSON, 72% schema-valid; every failure traced to the slots fixed above. At 1.1.1: 13/13 conformance re-runs schema-valid on both models.

## 1.1.0 — 2026-10-26

Driven by a simulation stress test of v1.0 (36 scenarios × 5 surfaces × 2 model tiers, graded blind). Breaking: teams must recompose and re-check their team prompts against the new output contract and scope.

**Breaking**
- `02` Part C (how to emit a response) moved out of Builder notes, so composition no longer strips it. Responses are JSON objects of typed parts. New `components/` folder: component library draft (`chat-components.md`) and `response.schema.json`. Parts-by-type table added.
- One chat across the platform: per-surface composition with a shared prefix (`prompts/platform.manifest.yaml`); the app passes the active surface each turn.
- Scope defined in `00`: platform only, broad within it, including the AI/ML/data/governance concepts needed for platform work. Out-of-scope requests are capability limits with no invented destination.
- `05`: "run", "experiment", "model", "version", "eval", "promote", "trial", "job" now have per-surface meanings. Removed "say 'let me try that'" (contradicted the banned opener).

**New**
- `06-platform-map.md`: surfaces, what each owns, destinations with approvers and what travels, no-destination fallback, policy and approval gates.
- Overlays: `experimentation` (Model Experimentation, Model Registry, Compute), `notebooks`, `governance`.
- Tone matrix rows: Policy or approval gate; Out of scope.
- `03`: Surfaces in one conversation; Actions across turns; Frustration.
- `04`: General knowledge level; Honest unknowns; Risk signals in content.
- Rubric: T7, T8, U7a/U7b (split), U29–U34, CF9, CF10, HO8; honest-unknown clauses on CF1, PL4, AC4, HO1, U8.

**Changed**
- Principle 4: past tense only after a tool confirms the action; everything else is offered.
- Principle 3: destinations come from the platform map or context; fallback when none.
- Type selection: approval gate step; "how did it do" → completion; capability leads when a search was also empty; approval-required chain; plan + question only when the plan can't proceed.
- `completion`: removed the "partially failed → error" contradiction.
- `confirmation`: reversibility may be unknown; an interpretation that changes the consequence shares the first sentence; side effects in user-authored code; reads are never confirmed.
- `handoff`: offered vs. sent; approval kind; examples rewritten so nothing claims to be sent before a tool confirms.
- `error`: generated code doesn't count against the budget; frustration folded into the lead; "continue" optional when continuing can't help.
- `data` overlay: sensitivity confirmation limited to writes/exports/sharing; column-meaning rule allows labeled name-based readings.
- `build` overlay and transcript: removed prose offers echoed by chips (SU4).
- `compose.py`: multi-surface output and a lint that fails if the output contract, scope, or destinations are missing.

## 1.0.0

Initial release: foundation, five shared modules, thirteen response types, three overlays (support, build, data), compose script, rubrics, two annotated transcripts.
