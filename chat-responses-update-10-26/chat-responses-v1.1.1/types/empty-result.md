---
type: empty-result
version: 1.0.0
component: text + action chips
situation: empty / nothing found
---

# Empty result

A search, query, lookup, or filter returned nothing. Says what was searched, that nothing matched, and how to widen or change the search — without implying anyone did anything wrong.

## Use when

- A catalog search, knowledge lookup, query, or filter returns zero results.
- A list the user asked for is empty (no runs yet, no test cases, no versions).
- A lookup for a specific object finds no match.

## Don't use when

- The search *failed* (timeout, error) → `error.md`. Empty means it ran and found nothing.
- The user isn't entitled to see results that exist → `access-and-capability.md`. Never disguise an access limit as an empty result — but also never reveal the existence of objects the user can't see. See rule 8.
- The assistant doesn't know how to search for this → `access-and-capability.md` (capability).

## Anatomy

1. **What was searched, and the result** (required) — one sentence, naming the scope and the terms exactly. "No datasets in `finance-prod` match `orders_eu`."
2. **Likely reason or nearest match** (optional, ≤1 sentence) — when the assistant can see one: a near-miss name, a scope that's too narrow, a filter that excluded everything.
3. **Ways forward** (required) — 1–3 actions: widen scope, try the near match, remove a filter, create the thing, ask a person.

## Length

≤2 sentences + actions.

## Tone

Empty: mid warmth, neutral. Not "unfortunately". Not apologetic. Nothing is wrong; there's just nothing there.

## Rules

1. Name what was searched — scope and terms — so the user can see whether the search was right.
2. Never "unfortunately", "sorry", "I couldn't find". State it: "Nothing matches…", "No runs yet."
3. Offer the nearest match when there is one, as a one-click option: "Did you mean `orders_eu_2025`?"
4. Offer to widen when the scope was narrow: other workspaces, a longer time window, fewer filters.
5. For empty lists of the user's own objects, the way forward is creation: "No test cases yet. [Save last exchange as a case]".
6. Never suggest the user misspelled or mis-asked. Offer the alternative without the diagnosis.
7. Never pad with what *was* found if it's irrelevant. "No match, but here are 20 other datasets" is noise unless they're near matches.
8. **Entitlements:** if objects exist that the user can't see, the assistant neither reveals them nor calls the result empty. It says what it can search: "Nothing in the workspaces you have access to matches `orders_eu`. If it's in another workspace, its owner can share it." Reconcile with the platform's entitlement disclosure policy.
9. When zero is the *answer* to a question ("how many failed?" → "None"), it's a direct answer, not an empty result.

## Components

Text; action chips; input request when offering near matches as options.

## Examples

### Good — near match
> No dataset named `orders_eu` in `finance-prod`. Nearest: `orders_eu_2025` (updated yesterday).
> [Use orders_eu_2025] [Search all workspaces]

Why it works: exact scope and term, the near miss with a useful fact, two ways forward.

### Bad
> Unfortunately, I couldn't find any datasets matching your search. Please check the spelling and try again, or contact your data steward for assistance.

What's wrong: "unfortunately", "couldn't", implies a typo, hands off with no context.

### Good — empty list
> No test cases yet for `Invoice triage`.
> [Save last exchange as a case] [Import from a suite]

Why it works: state plus the two ways the list gets its first item.

### Good — scope too narrow
> No failed runs in the last 24 hours. The last failure was 4 days ago (`Check PO`, 503).
> [Show last 7 days] [Open that run]

Why it works: the answer, plus the one fact that saves the next question.

### Good — entitlement-aware
> Nothing in the workspaces you have access to matches `pii_customers`. If it lives elsewhere, its owner can share it with you.
> [Request access by name]

Why it works: doesn't confirm or deny existence; gives the path.

## Anti-patterns

- **The apology** — "Sorry, no results."
- **The typo accusation** — "Please check your spelling."
- **The consolation dump** — "No match, but here are 47 other things."
- **The dead end** — "No results found." Full stop.
- **The leak** — "That dataset exists but you can't see it."

## Rubric

Checks `EM1`–`EMn` in `evals/rubrics.md` — the single source; rules here reference them, not the other way round.
