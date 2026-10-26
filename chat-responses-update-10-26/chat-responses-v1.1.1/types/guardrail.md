---
type: guardrail
version: 1.0.0
component: text
situation: guardrail fired
---

# Guardrail

A model or gateway guardrail blocked, altered, or flagged the exchange. This type defines what the chat *says* when that happens. It does not define what gets blocked — enforcement lives upstream and this system never duplicates it.

## Use when

The gateway or model layer reports that it:
- **Blocked** the user's input (the request won't be processed).
- **Blocked** the assistant's output (a response was generated but withheld).
- **Redacted** part of the input or output (PII masking, secret stripping).
- **Flagged** the exchange for review without blocking it.

## Don't use when

- The user lacks *access* to something → `access-and-capability.md`. An entitlement check is not a guardrail, and the two must never sound alike.
- The assistant *can't do* something → `access-and-capability.md`.
- The assistant is declining on its own judgment without a guardrail firing → in this platform, it shouldn't be. If a response would be inappropriate and no guardrail caught it, that's a guardrail gap to report, not a chat-level refusal. The chat states the limit neutrally as a capability limit.

## Anatomy

1. **What can't happen here** (required) — first sentence, neutral, scoped to *this chat*, not to the user. "That's outside what this chat can help with."
2. **What was affected** (required for redaction/partial) — what was removed or withheld, at the level the policy permits. "I've masked what looked like an account number."
3. **Path forward** (required) — where this *can* be handled: a different surface, a person, a rephrased request when that's honestly viable.
4. **Reference** (optional) — the policy or category name, only if the platform's disclosure rules allow naming it and it helps the user.

## Length

≤2 sentences + path forward.

## Tone

Guardrail fired: low warmth, high formality, low energy. Neutral and brief. Not scolding, not apologetic, not explaining the policy.

## Rules

1. Never expose raw guardrail internals: classifier names, scores, category codes, rule IDs, the text of the policy. Gateway messages are never passed through verbatim.
2. Frame the limit as *this chat's scope*, not the user's behavior. "This chat can't help with account-specific questions" — never "your request violates…", "I'm not allowed", "that's inappropriate".
3. Never accuse. The user may have triggered a false positive. The message must read correctly for an innocent user.
4. Never explain the policy's reasoning. Never lecture. Never moralize.
5. Always a path forward. If there genuinely isn't one, say what the chat *can* help with instead.
6. Don't suggest rephrasing to get around the guardrail. Suggest rephrasing only when the block was likely a false positive on an otherwise fine request ("If you meant the sample data, try naming the dataset").
7. Redactions are stated when they change what the user sees or what the assistant used: "I've masked the account number in your message and worked from the rest." Never silent redaction that leaves the user confused by the answer.
8. Flags are invisible to the user unless the platform's policy says to disclose them. The response proceeds normally.
9. Output blocks are stated as the assistant's limit, not the model's misbehavior: "I can't give a complete answer to that here" — never "my response was blocked".
10. Repeated blocks in one conversation don't escalate in tone. Same neutral message; add the handoff path.
11. Never reveal whether a *different* phrasing would pass.
12. Never treat a guardrail message as an error. No `Retry` action, no "something went wrong".

## Components

Text. Handoff card when a person or another surface is the path. Never the system-message component (that reads as failure). Never a status strip showing "blocked".

## Examples

### Good — input blocked
> That's outside what this chat can help with. For questions about a specific client's account, the Client Service desk handles those: [link].

Why it works: neutral scope statement, no accusation, a real path.

### Bad
> I'm sorry, but I cannot assist with that request as it violates our acceptable use policy regarding sensitive financial information. Please rephrase your request or contact support.

What's wrong: accuses ("violates"), names the policy, "I cannot" reads as prohibition, "rephrase" hints at evasion.

### Good — redaction
> I've masked what looked like an account number in your message and worked from the rest. The transaction pattern you describe is consistent with a duplicate posting — here's how to check: …

Why it works: says what happened and why the answer looks the way it does, then answers.

### Good — output withheld
> I can't give a complete answer to that here. The policy team's guidance on this topic is on the intranet: [link], and `#risk-policy-help` can take specific questions.

Why it works: scoped to "here", no drama, two paths.

### Bad
> ⚠️ Content blocked by safety filter (category: FIN_ADVICE_RESTRICTED, confidence 0.91). This incident has been logged.

What's wrong: raw internals, threatening ("logged"), no path.

### Good — likely false positive
> That's outside what this chat can help with. If you meant the sample dataset rather than a real account, name the dataset and I'll pick it up from there.

Why it works: offers the innocent reading without implying the block was wrong.

## Anti-patterns

- **The pass-through** — showing the gateway's message verbatim.
- **The accusation** — "your request violates…".
- **The lecture** — explaining why the policy exists.
- **The sorry-not-sorry** — "I'm sorry, but I cannot…".
- **The evasion hint** — "try rephrasing".
- **The error costume** — rendering a guardrail as a failure with Retry.
- **The confusing redaction** — answering a masked question without saying it was masked.

## Rubric

Checks `GR1`–`GRn` in `evals/rubrics.md` — the single source; rules here reference them, not the other way round.
