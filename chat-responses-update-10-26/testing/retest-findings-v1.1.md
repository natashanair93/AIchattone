# Chat responses — v1.1 retest and v1.1.1 changes

Round one found that v1.0's voice was solid but the system couldn't stretch across Fusion: no output contract once composed, one chat per surface, no scope policy, and rules that contradicted each other. v1.1 fixes those and was retested on 18 scenarios written independently. **On those unseen scenarios v1.1 passed 17/18 on the strong model and 18/18 on the small one, against 15/18 for v1.0.** Off-platform requests are now declined, approval gates route to Governance, and no platform fact was invented. The output contract needed one more pass: every response was valid JSON, but 28% broke the strict schema on slots the prompt hadn't spelled out. 1.1.1 fixes that, and 13 of 13 re-runs now validate.

## What the retest shows
- **The gain on unseen scenarios is real but modest** — v1.0 was already decent on many cases. The three v1.0 failures were exactly the gaps v1.1 closed: it wrote a wedding toast (scope), presented a $615 sweep without stating the charge is irreversible (spend), and left reversibility out of a ticket confirmation.
- **The small model held up on v1.1**: 18/18 on unseen scenarios, mean quality 3.62 vs. 3.81 for the strong model. If cost pushes Fusion toward a smaller model, the rules carry over.
- **The original set went from 25/36 to 36/36**, but read that with care: round one batched scenarios (which leaked details between them) and graded against v1.0's rules. Round two ran each scenario in a fresh session and graded against v1.1. The holdout set is the fairer comparison.
- **The one v1.1 failure** (H6, strong) offered an MRM handoff without saying what sending it would do. It also showed a pattern the rules don't yet cover: nudging an approval that is already in flight.
- **Format:** 100% of v1.1 responses were valid JSON on both models. 72% passed the strict schema. Every failure traced to slots the compact contract didn't spell out: object types, the field for a button's role, metric shape. 1.1.1 lists them, and a 13-response conformance re-run on both models passed 13/13.
- **Governance**, a surface round one never tested, passed 6/6 on v1.1 across both models — including the scenario where no completion date existed and the chat had to say so instead of inventing one.

## From finding to fix

| Finding | Change | Retest evidence | Status |
|---|---|---|---|
| F-01 Output contract stripped | Part C moved into the prompt; JSON parts; compose.py fails if it's missing; component library draft + schema | 72/72 valid JSON. 72% schema-valid at 1.1.0 → 13/13 at 1.1.1 | Fixed |
| F-02 One chat per surface | Platform map; per-surface composition with a shared, cacheable prefix; Notebooks, Experimentation, Governance overlays; terms that change by surface | B5 explains ML experiment vs. run correctly and notes the Agent Studio meaning; Governance 6/6 | Fixed |
| F-03 Did / will | Past tense only after a tool confirms; handoff offered vs. sent | 0 did/will failures (U6). E3 now offers the ticket instead of claiming it. One HO8 miss (H6) | Fixed |
| F-04 Scope undefined | Platform-only scope in foundation, with AI/ML/data concepts in scope when they serve platform work | Wedding toast, self-review, VaR theory, vendor-email summary all declined by v1.1; v1.0 wrote the toast | Fixed |
| F-05 No destination fallback | Platform map destinations + fallback rule | B4/H6 route to Governance › MRM; 0 invented teams or destinations | Fixed |
| F-06 Rubric fails good answers | Honest-unknown clauses; U7 split into platform facts vs. general knowledge; code excluded from budgets | C4 and D6 now pass with reversible: unknown; B3's labeled general ML advice passes | Fixed |
| F-07 Contradictions | 'Let me' removed from 05; completion/error line fixed; echo examples rewritten; approval-required chain; sensitivity reads not confirmed; frustration folded into the lead | D2 no longer claims Confidential reads need confirming; A4 handled as approval chain | Fixed |
| F-08 Side effects in user code | Confirmation covers user-authored code; CF9 | C4 confirmed with skip-cell alternative on v1.1 | Fixed |
| F-09 Risk signals in content | Rule in 04 + U33 | F1 v1.1 declines the summary but still flags the bank-detail change | Fixed |
| F-10 Small model over-uses components | Parts-by-type table; status only on runs | 0 status-strip misuse on v1.1 small; 18/18 holdout | Fixed |
| F-11 Frustration inconsistent | Frustration section in 03; U32 | U32 flagged twice on strong; graders split on whether a direct 'Yes' counts as acknowledgement | Partly |

## New from the retest
- **The compact contract under-specified enums and object shapes** (P1, G) — Models invented object types ('use case', 'MRM validation') and named a button's role field themselves ('role'). JSON was always valid; strict schema validity was 72%. *Status:* Fixed in 1.1.1: enums, button objects, metric and starter shapes listed in the prompt; 13/13 conformance re-runs valid.
- **Pattern-library behaviors that clash with the response rules** (P1, G) — Suggested follow-ups auto-dismiss after 10s and hide on errors, but error replies depend on chips for the way forward. The typing indicator's rotating text can drift into filler. 'Mode' meant two things. *Status:* Proposed in the components draft: split prompt pills from persistent action buttons; drive the indicator from progress labels; rename 'mode' in the response rules. Needs the design system owner's decision.
- **No pattern for nudging an approval already in flight** (P2, G) — H6: a model already in MRM validation, needed by Friday. The rules cover requesting an approval, not chasing one. *Status:* Open: add an 'in-flight approval' example to handoff.md (status, who holds it, what the user can send, no ETA unless known).
- **U32 (frustration) may be too literal** (P2, R) — Graders disagreed on whether an immediate 'Yes — a person is next' counts as acknowledgement. *Status:* Open: reword U32 to accept an immediate direct answer to the user's demand as acknowledgement.
- **Test runners with broad tools wander** (P2, H) — A few small-model run agents made unrelated tool calls (three scheduled 'placeholder' messages, a clipboard read). It doesn't affect results but matters for whoever re-runs this. *Status:* Runner now restricted to read and write. Use a plain API harness in your environment.