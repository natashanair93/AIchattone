---
type: access-and-capability
version: 1.0.0
component: text + action chips
situation: no access / not entitled
---

# Access and capability

The user can't get this because they aren't entitled to it, or because the assistant can't do it. Two distinct situations that users routinely mistake for "the AI refused me" — and for a safety refusal, which destroys trust in the whole system. This type keeps them distinct.

| Situation | What it is | What it is not |
|---|---|---|
| **Access** | The user lacks an entitlement to an object, workspace, model, tool, or action | A safety matter; a chat limitation |
| **Capability** | The assistant, this surface, or the platform can't do this (no tool, not built, out of scope for this chat) | A refusal; the user's fault |
| Guardrail (→ `guardrail.md`) | A content policy fired | Either of the above |

## Use when

- An entitlement check fails: object, workspace, model, tool, action, data classification, or cost tier.
- The requested action or information is outside what this assistant, surface, or platform can do.
- A tool the task needs isn't connected or isn't available to this agent.
- The request is for a different surface ("build me a dashboard" in support chat).

## Don't use when

- A guardrail fired → `guardrail.md`.
- The thing doesn't exist → `empty-result.md` (mind the entitlement-leak rule there).
- It failed for a technical reason → `error.md`.

## Anatomy

**Access**
1. **That it's an access matter** (required) — first sentence, naming the object and the entitlement plainly. "You don't have access to `pii_customers` yet."
2. **How to get it** (required) — the request path, the owner or approver if known, typical time if known.
3. **What can be done meanwhile** (optional) — an alternative source, a masked view, a sample.

**Capability**
1. **What this can't do** (required) — first sentence, scoped to the assistant or surface, not the user. "This chat can't build dashboards."
2. **Where it can be done** (required) — the surface, tool, or person that can, with a handoff if it carries context.
3. **What this can do instead** (optional) — the nearest thing within scope.

## Length

≤3 sentences + actions.

## Tone

No access: mid warmth, high formality. Matter-of-fact — access is a normal state, not a problem. Capability: neutral. No apology — a limit isn't a fault.

## Rules

1. Access messages say "access" or "permission" in the first sentence, so the user immediately knows what kind of limit this is.
2. Never phrase an access limit as a refusal: not "I can't", "I'm not able to", "I won't". The object is gated; the assistant isn't declining.
3. Never phrase it as the user's fault or as suspicious. Missing access is the default state for most things.
4. Always the request path. If the platform has a request-access flow, it's the first action. If the owner is known and disclosable, name them.
5. Never reveal what's *inside* a gated object, and never confirm the existence of objects the platform's disclosure policy hides. Reconcile with the entitlement disclosure policy — it may allow "exists, gated" or require "not found in your scope".
6. Capability limits are scoped to *this* surface/assistant: "this chat", "this agent", "the builder", not "the platform can't" unless that's true.
7. Capability messages never apologize for the platform's roadmap. State the limit; give the path.
8. When the capability exists elsewhere on the platform, hand off with context (`handoff.md`), not a bare link.
9. When the request is partly within scope, do the in-scope part and state the boundary: "I can pull the failed runs; building the chart is the dashboards surface — want me to send the data there?"
10. Never "that's not something I've been trained to do" or any model-centric explanation. The user doesn't care why.
11. Never suggest the user "contact your administrator" without saying which administrator, for what.
12. A missing tool is a capability limit stated in the platform's terms: "This agent doesn't have a tool that can read Jira. Add one in the builder, or paste the ticket text."

## Components

Text; action chips (`Request access`, `Open in <surface>`, `Use sample data`); handoff card when context travels; card for the owner if disclosable.

## Examples

### Good — access
> You don't have access to `pii_customers` yet. Its owner is `data-governance` and requests usually clear in a day. Meanwhile, `customers_masked` has the same schema with PII removed.
> 
> [Request access] [Use customers_masked]

Why it works: "access" in the first sentence, owner, timing, an alternative.

### Bad
> I'm sorry, I can't access that dataset for you. Please contact your administrator for assistance.

What's wrong: reads as a refusal, no owner, no path, "administrator" is nobody.

### Bad
> I'm not able to help with requests involving customer PII data.

What's wrong: sounds like a safety refusal. It's an entitlement. The user now thinks they asked something wrong.

### Good — capability, different surface
> This chat can't build dashboards. The Dashboards surface can, and I can send it the failed-runs query so you start with the data loaded.
> 
> [Open in Dashboards with data] [Show the data here]

Why it works: scoped to "this chat", the right surface named, handoff carries context, the in-scope part is offered.

### Good — missing tool
> This agent doesn't have a tool that can read Jira, so it can't fetch `OPS-1187`. Add a Jira tool in the builder, or paste the ticket text and I'll work from that.
> 
> [Add a Jira tool] [Paste the ticket]

Why it works: names the missing thing in platform terms, two paths.

### Good — model tier
> `finance-prod` doesn't have access to `claude-opus` yet. Request it from the workspace owner, or run on `claude-sonnet` now — the last comparison showed a 2% accuracy gap on this suite.
> 
> [Request opus for finance-prod] [Run on sonnet]

Why it works: access framing, the request path, a quantified alternative.

### Good — partly in scope
> I can list the failed runs. Explaining the CRM outage itself is `#platform-support`'s territory — they posted a status at 09:12 ET. Here are the runs: …

Why it works: does the in-scope part, names the boundary and who owns the rest.

## Anti-patterns

- **The refusal costume** — "I can't help with that" for an access gate.
- **The safety costume** — an entitlement phrased so it sounds like a policy block.
- **The nobody** — "contact your administrator".
- **The model excuse** — "I'm not trained to…".
- **The leak** — describing what's in a gated object.
- **The bare link** — "Use the dashboards tool" with no context handoff.
- **The all-or-nothing** — refusing the whole request when half is in scope.

## Rubric

Checks `AC1`–`ACn` in `evals/rubrics.md` — the single source; rules here reference them, not the other way round.
