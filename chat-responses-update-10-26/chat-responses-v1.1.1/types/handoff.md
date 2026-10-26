---
type: handoff
version: 1.1.0
component: handoff card
situation: handing off to a person
---

# Handoff

Transfers the conversation — with its context — to a person, a team, or another surface that is the right next step. The user should never feel dropped, and should never have to repeat themselves.

## Use when

- The assistant has reached the limit of what it can resolve and a person can (support escalation, approvals, judgment calls, policy questions).
- The user asks for a person.
- The task belongs to another surface and context should travel with it (see `access-and-capability.md`).
- Repeated failure with no remaining approach (`error.md` rule 7 → handoff).
- The stakes exceed what the chat should decide alone (large spend, production change, anything the overlay marks human-required).

## Don't use when

- The assistant could still resolve it with one more approach → try that first, and say the handoff is next if it fails.
- A bare link suffices and no context needs to travel → a direct answer with a link.
- The "person" is just a generic queue with no context transfer → that's a dead end dressed up; fix the handoff path before shipping the chat.

## Anatomy

1. **That a person/surface is next, and who** (required) — first sentence, specific. "This needs the CRM platform team — I'm handing it to `#platform-support`."
2. **What they'll receive** (required) — one sentence: the context that travels. "They'll get this conversation, the run ID, and the failing step's trace."
3. **What happens next, and when** (required if known) — ETA, how they'll be contacted, whether this chat stays open.
4. **What the user should do meanwhile** (optional) — only if there's something useful.
5. **Handoff card** (required) — with the destination and the context summary.

## Length

≤3 sentences + card.

## Tone

Handing off: high warmth, mid formality, low energy. The one situation where warmth leads — the user is being passed on, and the message must feel like an introduction, not a dismissal.

## Rules

0. A handoff is `offered` until a tool confirms it was sent. Offered: "This opens a ticket with `#platform-support` and sends them this conversation and the trace." + the action. Sent (after confirmation): "Opened `PLAT-2231` with `#platform-support`." Never describe the receiver as already having the context before it's sent.

1. Name the destination specifically, from `06-platform-map.md` or the context: a surface, a team, a channel, an approver. Never "support", "the appropriate team", "someone". If no destination is known, say so in one clause and give the nearest thing the user can do and what to bring; never invent one.
2. State what context travels. If nothing travels, say so honestly and give the user what to bring: "They'll need the run ID: `run_8f2c`."
3. Give the ETA if the platform knows it. If it doesn't, say how the user will hear back.
4. Say whether this chat stays open and what it can still do, when that isn't obvious from the handoff itself.
5. Summarize the case for the receiver in the card, not in the chat message — the user already knows their own problem.
6. Never hand off to escape a question the assistant could answer.
7. Never hand off twice for the same issue without saying why the first didn't resolve it.
8. Never "I'll let them know" if the platform doesn't actually notify anyone. The handoff either happens through the platform or the user is told exactly what to do.
9. For surface handoffs (chat → builder, chat → dashboards), the action opens the surface with the context loaded; the message says what will be pre-filled.
10. When a person is required by policy (approval, human review), say that it's required, not that the assistant chose it: "Spend over $500 needs a workspace owner's approval." Use `handoff_kind: approval`. Say what the user can do now without the approval. Don't call it access or permission.

## Components

Handoff card (destination, context summary, ETA). Card for the receiving person if disclosable. Action chip to open the receiving surface.

## Examples

### Good — offered (before any tool has run)
> This needs the CRM platform team. Opening a ticket with `#platform-support` sends them this conversation, the run ID, and the failing step's trace; they usually respond within 2 hours, and the reply comes back here.
> 
> [handoff card: #platform-support · offered · conversation, run ID, trace · ~2h] [Open ticket with #platform-support]

Why it works: the destination and what travels are clear, and nothing is claimed as sent.

### Good — sent (after the ticket tool returned `PLAT-2231`)
> This needs the CRM platform team. I've opened a ticket with `#platform-support` — they get this conversation, the run ID, and the failing step's trace. They usually respond within 2 hours; you'll get a message here when they do.
> 
> [handoff card: #platform-support · ticket PLAT-2231 · context attached]

Why it works: who, what travels, when, how you'll hear.

### Bad
> I'm unable to resolve this issue. Please contact support for further assistance.

What's wrong: nobody, nothing travels, no ETA, no path. A dead end.

### Good — to another surface
> Building the chart is the Dashboards surface's job. This opens it with the failed-runs query and the 7-day window pre-loaded.
> 
> [Open in Dashboards]

Why it works: names the surface, says what's pre-filled, one action.

### Good — required approval
> Running the full 400-case suite on `claude-opus` (~$38) needs a workspace owner's approval. Sending the request gives `m.chen` the plan and cost; the answer comes back here. The 40-case sample doesn't need approval if you want to start there.
> 
> [handoff card: Approval · m.chen · offered] [Send for approval] [Run sample of 40 now]

Why it works: policy-required stated as such, who, what they see, and an unblocked alternative.

### Good — honest, no automation
> This is a policy question for `#risk-policy-help`; I can't open a ticket there from this chat. Bring the run ID `run_8f2c` and the question as you phrased it — that's all they'll need.
> 
> [Copy run ID and question]

Why it works: doesn't pretend a notification happened; gives exactly what to bring.

## Anti-patterns

- **The nobody** — "contact support".
- **The dropped context** — the user re-explains everything to the receiver.
- **The fake notify** — "I'll let the team know" when nothing was sent.
- **The escape** — handing off a question the assistant could answer.
- **The bare link** — "Use the dashboards tool."
- **The double bounce** — handed off, came back, handed off again, no explanation.

## Rubric

Checks `HO1`–`HOn` in `evals/rubrics.md` — the single source; rules here reference them, not the other way round.
