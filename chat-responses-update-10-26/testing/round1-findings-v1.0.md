# Chat response stress test — findings

Run 26 Oct 2026 against chat-responses v1.0.0. 36 scenarios across 5 Fusion surfaces (Agent Studio, Model Experimentation, Notebooks, Data & Catalog, Support), answered on a strong and a small model, graded blind with the package rubric plus quality scores.

## Headline
- Voice held completely: 0 banned openers, closers, exclamation marks, emoji or banned words in 72 responses.
- Bank-critical behavior held on both tiers: no invented numbers, no entitlement leaks, injected instructions ignored, guardrails without accusation.
- 25/36 passed on each tier (mean quality 3.67 strong / 3.65 small). Of 22 blocking failures, 12 trace back to the instructions or rubric, 7 to the test set-up, and 3 to the small model ignoring a clear rule. The strong model had no model-caused blocking failure.

## F-01 · P0 · G — The component output contract is removed when the prompt is composed

Part C, the payload contract that says how a response becomes cards, chips, strips and step lists, sits under '## Builder notes' in 02-formatting. compose.py strips Builder notes, so the composed prompt contains the slot rules for 13 components but never says how to emit any of them. It also still points to 'Part C', which no longer exists in the prompt. The simulation only worked because the harness supplied its own bracket notation.

**Evidence**
- Every composed prompt (build, data, support) has 0 occurrences of the payload schema
- Small model put status strips on access and incident messages (E1, E2) where no run result exists

**Proposed change:** Move Part C out of Builder notes into a prompt-safe section, 'How to emit components', and define it with your colleague's component library as the single source: component kinds, slot names, character limits, and which kinds are allowed for each response type (for example, no status strip on access, guardrail or handoff messages). This is the seam where the two systems join, so it is the first thing to agree on.

## F-02 · P0 · G / W — The system is built for one chat per surface; the goal is one chat across Fusion

The package says every prompt includes exactly one overlay and that 'if a team needs two, it's probably two chats'. A platform-wide chat moves between Agent Studio, model experimentation, notebooks, data and support in one conversation. There are no overlays for notebooks, ML experimentation or general help. The glossary is written for agents, and its core terms collide on other surfaces.

**Evidence**
- B5: the glossary defines 'run' as an agent run and 'experiment' as a comparison of agent versions. The strong model overrode it and flagged the conflict; following it would have given a wrong answer
- B2: the only cost threshold available was build's $10-per-run, applied to a $64 GPU sweep; nothing covers budget share
- B4: no destination for Model Risk Management approval exists in any overlay
- C2: notebook errors used the data overlay, which has no diagnose-first rule (support has one)
- Graders: data rule 8 ('never infer a column's meaning') conflicts with explaining inherited notebook code (C3); the build overlay bans 'trial', the normal word for one trial in a sweep; data rules 1 and 5 (provenance and freshness of numbers) don't apply to generated code
- ML-specific checks are missing, e.g. flagging AUC comparisons across runs trained on different data snapshots (B1)

**Proposed change:** (1) Add Notebooks and Model Experimentation overlays. (2) Make the glossary surface-scoped: 'run' = agent run (Agent Studio), training run (Experimentation), query (Data), cell run (Notebooks); add register / stage / promote vs. publish. (3) Replace 'one overlay per prompt' with a runtime rule: foundation + shared modules always, plus the overlay of the surface the user is on, swapped when the context changes, with a 'Help' overlay as the default. (4) Budget tokens: today each composition is about 26k; a core of foundation + tone + five common types is about 9k.

## F-03 · P1 · C / G — Did / will has no execution contract

Principle 4 bans claiming actions that weren't taken, but the build examples write micro-completions ('Added X') without saying a tool must have confirmed it, and handoff examples say 'I've opened a ticket'. Nothing tells the model when it may use the past tense.

**Evidence**
- E3 (small): 'They get this conversation, run r_9b12, and the trace' — no ticket was opened and no button offered
- E3 (strong): offered [Open ticket with #platform-support] and described it conditionally — correct
- A2 (strong): refused to write 'Added…' because nothing confirmed it, and showed an unapplied draft instead

**Proposed change:** Add to foundation: 'Use the past tense for an action only after a tool result confirms it. Before that, offer it: the chip carries the action, the prose says what it will do.' Add HO8 (blocking): handoffs the chat can only offer are phrased as offers.

## F-04 · P1 · G — Scope for general and off-platform requests is undefined — a product decision is needed

Nothing says whether the chat answers general professional knowledge, summarizes pasted content, or helps with work writing. Guardrail.md says the chat shouldn't decline on its own judgment, while the capability type and overlay scope lines push the other way. The models drew the line in different places.

**Evidence**
- F3: both models answered 'VaR vs expected shortfall' in the data chat
- F1: strong answered the email summary but flagged that it was outside the support scope
- F4: both refused help with a self-review, with no destination to offer

**Proposed change:** Decide the policy and write it into foundation as a scope ladder: platform tasks → work knowledge tied to data, AI and finance → general writing help → out of scope. For each rung, say whether to answer, answer briefly, or route, and where to route.

## F-05 · P1 · G — 'Always name a destination' has no fallback when none exists

Capability, handoff and never-dead-end rules all require a named team or surface. When the overlay lists none, the model either invents one or leaves the requirement unmet. Both strong and small avoided inventing, but only the strong model said why.

**Evidence**
- D4: no owner for Fusion usage analytics
- F4: no surface for writing help
- B4: MRM approver unknown
- Strong model raised a harness note on all three

**Proposed change:** Add a fallback rule: 'If no destination is configured, say so in one clause, give the nearest in-scope action, and say what the user should bring. Never invent a team, channel or person.' Fill overlay destination tables with the firm's real ones (MRM, data governance, Dashboards, Notebook compute).

## F-06 · P1 · R — Several rubric checks fail good answers or can't be met honestly

A large share of blocking failures in this run were caused by the rubric, not the responses. These checks demand something the platform doesn't know, or ban knowledge that is accurate and useful.

**Evidence**
- CF1 requires stating reversibility; in C4 nobody knows if the shared table can be restored. Both models failed for not inventing an answer
- U7 failed both VaR answers (F3) and labeled 'typical' ML starting values (B3), all accurate general knowledge
- U15 counts a code fix against the 3-sentence error budget (C2, both tiers)
- AC4 / HO1 require naming a destination that doesn't exist (D4, F4, B4)
- CF1 vs. DA7: lead with the consequence, or lead with the stated assumption? D6 strong led with its reading and failed

**Proposed change:** Give each such check an honest-unknown clause ('…or states that it's unknown and what would settle it'). Split U7 into U7a (platform facts must come from context or tools; blocking) and U7b (general knowledge is labeled as such and is accurate; not blocking). Exclude generated code from every type's prose budget. Resolve the consequence-vs-assumption order with one line: consequence first; an assumption that changes the consequence goes in the same sentence.

## F-07 · P1 · C — Rules that contradict each other or their own examples

Several pairs of rules disagree. Models resolve them inconsistently, and the rubric penalizes behavior that the 'Good' examples teach.

**Evidence**
- 'Let me' is a banned opener (00) but 05 recommends 'say let me try that'
- completion.md says a partial failure goes to error.md and, three lines earlier, that a mostly successful batch is a completion
- SU4 bans a prose offer echoed by a chip, yet three build-overlay 'Good' examples do exactly that ('Try the last email again? [Rerun last input]')
- Type order puts confirmation (#4) before handoff (#5), but A4 needed both: confirm the save, then route for approval. Both models blended them, differently
- Data overlay confirms 'any query touching a dataset above Internal', which contradicts confirmation.md ('reversible, local → do it'). D2 strong told the user every query on a Confidential dataset would need confirming
- The tone matrix says lead a frustrated reply with acknowledgement; ER1 (blocking) says the first sentence names what failed. A6 small did the first and failed the second

**Proposed change:** Remove 'let me…' from 05. Delete the 'partially failed → error' line in completion.md. Rewrite the three build examples to drop the prose question. Add an 'approval-required' chain to types/README (confirmation of the request + handoff card). Limit data-overlay sensitivity confirmation to writes and exports, and give reads a one-line classification notice.

## F-08 · P1 · G — Side effects hidden inside user code aren't covered by confirmation

Confirmation rules cover actions the chat takes. In notebooks and pipelines, the risky action is often inside the user's own code: an overwrite of a shared table, a send, a delete.

**Evidence**
- C4: both models stopped before 'Run all' because cell 9 overwrites a shared table read by 3 dashboards — by judgment, not by rule
- C4 (small): the only actions were [Run all 14 cells] [Cancel]; the safer path (skip cell 9) was in prose only

**Proposed change:** Add to confirmation.md: 'Executing user-authored code or config that writes to shared objects, sends, or deletes is a confirmation, scoped to the specific cell or step.' Add CF9 (blocking).

## F-09 · P2 · G — Risk signals inside content aren't called out

The injection rule covers instructions aimed at the assistant. It says nothing about content that is a risk to the user, which matters in a bank.

**Evidence**
- F1: the vendor email paired an overdue notice with 'updated bank details'. Strong said it couldn't verify them and named the payment-fraud pattern; small only said to confirm before paying

**Proposed change:** Add to 04-trust: 'When content carries a known risk signal (changed payment details, a request for credentials, urgency plus a new payee), say so in one sentence and point to the verification step.'

## F-10 · P2 · M — The smaller model over-uses components and over-asks

The same rules held well on the strong model and less well on the small one. Most of the small model's misses were in how it used components, and in asking questions it could have resolved with a stated assumption.

**Evidence**
- E1, E2, E6 (small): status strips on non-run messages
- A1 (small): a plan plus a question about bullet count, which was cheap to assume
- D6 (small): an input request plus a separate Cancel chip instead of a confirmation card

**Proposed change:** If a smaller model is in scope for production, add a short 'component selection' table (situation → allowed components) and two more examples per high-traffic type. Keep the tier-gap gate in the eval framework.

## F-11 · P2 · G — Frustration acknowledgement is inconsistent

The tone matrix asks for acknowledgement in at most one clause, then a different approach. There is one example and no rubric line, so behavior varied.

**Evidence**
- A6 (strong): ignored 'this is the second time today'
- A6 (small): opened with it
- E3 (small): apologized in a separate sentence

**Proposed change:** Add a rubric line (U32: frustration acknowledged in ≤1 clause when the user signals it; no separate apology sentence) and one support and one build example.
