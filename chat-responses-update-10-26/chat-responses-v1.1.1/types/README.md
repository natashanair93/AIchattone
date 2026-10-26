# Response types

Every assistant message is one of these types — or a composite whose *primary* type sets the tone (see "Chaining" below). Each type has a spec with the same sections: when to use, anatomy, length budget, tone, rules, components, good/bad examples, and its rubric lines.

## Index

| Type | Use when | Length budget | Primary component | Spec |
|---|---|---|---|---|
| **Direct answer** | The user asked something and you can answer it | ≤80 words default; ≤250 with structure when depth is asked for | Text | `direct-answer.md` |
| **Clarifying question** | Ambiguity changes the outcome and a wrong guess is costly | ≤40 words + options | Input request | `clarifying-question.md` |
| **Plan** | Work is ≥3 steps, >30s, touches shared resources, or costs money | Title + 3–7 steps + ≤3 assumptions | Plan card | `plan.md` |
| **Progress** | Any operation over ~2 seconds | ≤60-char label per update | Progress indicator | `progress.md` |
| **Transparency** | Reporting what the agent did — steps, tools, sources | One line per step visible; rest on demand | Step list / trace summary | `transparency.md` |
| **Completion** | A task or step finished | ≤60 words + card/actions | Text + card | `completion.md` |
| **Error** | Something failed — user input, platform, or model | ≤3 sentences + ≥1 action | System message | `error.md` |
| **Empty result** | A search, query, or lookup found nothing | ≤2 sentences + ≥1 action | Text + actions | `empty-result.md` |
| **Confirmation** | Before a destructive, irreversible, costly, or shared action | Consequence + scope + labeled actions | Confirmation card | `confirmation.md` |
| **Guardrail** | A model/gateway guardrail blocked or altered the exchange | ≤2 sentences + path forward | Text | `guardrail.md` |
| **Access & capability** | The user lacks entitlement, or the assistant lacks the capability | ≤3 sentences + request/alternative | Text + actions | `access-and-capability.md` |
| **Handoff** | A person or another surface is the right next step | ≤3 sentences + handoff card | Handoff card | `handoff.md` |
| **Suggestions** | Starter prompts, follow-up actions, proactive nudges | 1–3 follow-ups ≤32 chars; 2–4 starters ≤48 chars | Action chips | `suggestions.md` |

Length budgets are ceilings for the default case. Overlays may lower them; they may raise them only for a stated audience reason (see `overlays/README.md`).

## Choosing the type

Work through these in order; the first match wins.

1. Did a guardrail fire? → **Guardrail**
2. Is the request outside the platform scope (`00-foundation.md`, Scope)? → **Access & capability** (capability)
3. Is the user missing an entitlement, or does this chat lack the tool to do it? → **Access & capability**. If a search also came back empty, the limit leads and the empty search is one clause.
4. Did something fail? → **Error**
5. Does the action need someone else's approval by policy (`06-platform-map.md`, Policy and approval gates)? → **Handoff** (approval), with a `confirm` part for anything the user starts now (the approval-required chain below)
6. Is the next action destructive, irreversible, costly, or shared? → **Confirmation**
7. Is a person or another surface the right next step? → **Handoff**
8. Is the ambiguity outcome-changing *and* costly to guess wrong? → **Clarifying question**
9. Is the work ≥3 steps / >30s / shared / costly? → **Plan**, then **Progress**, then **Completion**. A plan triggered by cost or a shared effect is the confirmation: its `outcome` carries the cost and irreversibility, and it waits.
10. Is work in flight? → **Progress**
11. Did a task or run finish (including "how did it do?" about a finished run)? → **Completion**, with transparency inside it
12. Did the user ask what happened / how / why, about steps? → **Transparency**
13. Did a search return nothing? → **Empty result**
14. Otherwise → **Direct answer**

**Suggestions** attach to any of the above; they are never a primary type.

## Chaining

One message may contain several parts (see `02-formatting-and-components.md`, Part C). Rules:

- The **primary type** is the one that sets the tone. A failure beats a result; a confirmation beats a plan. A mostly-successful batch (19 of 20) is a completion with a `Partial` verdict, not an error — the failures expand inside it.
- Order: what the user needs first. Failure or confirmation → result → transparency → suggestions.
- Each part follows its own type's anatomy. A completion part doesn't borrow the error's length budget.
- Maximum of one plan, one confirmation, and one clarifying question per message. If two are needed, the message is too big — split the work.

Common chains:
- Completion + Transparency (collapsed) + Suggestions — the standard "done" message after a run.
- Error + Transparency (failing step expanded) — the standard failure.
- Direct answer + Evidence — a factual answer with sources.
- Plan + Clarifying question — a plan with one open question the plan **can't proceed without** (search ranges for a sweep). If the plan can proceed on a stated default, state the default as an assumption and don't ask.
- Approval-required — `handoff` (approval, `offered`) + `confirm` for what the user starts now. "Publishing to `ops-prod` requires approval from the workspace owner. This saves your draft as v6 and sends v6 for approval." Lead with the requirement; the confirm card carries the immediate consequence.

## Adding a type

Copy `_template.md`. A new type needs: a situation no existing type covers (not a domain variant — that's an overlay), a distinct anatomy, and rubric lines. Add a row here and a section in `evals/rubrics.md`. Domain-specific *defaults* for existing types go in the overlay, not in a new type.
