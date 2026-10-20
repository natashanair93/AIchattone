---
type: suggestions
version: 1.0.0
component: action chips
situation: attaches to the primary type's situation
---

# Suggestions

Starter prompts, follow-up actions, and proactive nudges. Never a primary type — suggestions attach to another response or to an empty state. Their job is to make the useful next step one tap away, and to teach what the chat can do without a manual.

Three kinds:
- **Starters** — in the empty state, before the first message.
- **Follow-ups** — beneath a reply: the next thing the user probably wants.
- **Nudges** — the assistant noticed something worth doing that the user didn't ask about.

## Use when

- **Starters:** first-run or empty session, when the surface has a clear set of things it's for.
- **Follow-ups:** the reply leaves an obvious, useful next action the user might not know is one tap away — run it, save it, compare it, open it.
- **Nudges:** the assistant has *evidence* of something worth acting on (a step that's 71% of cost; a suite that hasn't run since the last version; a test case that would capture the exchange just had). Not general tips.

## Don't use when

- The reply already names the next step in prose → don't repeat it as a chip. Pick one place.
- There's no clear next step → no chips. Empty is better than filler.
- The suggestion is a sales pitch for a feature → that's marketing, not a nudge.
- The next step is consequential → that's a `confirmation.md`, not a chip.

## Anatomy

**Starters**
1. 2–4 chips, each a complete request the user could have typed, ≤48 chars, in the user's voice, drawn from what this surface actually does. Prefer ones that use the user's real objects: "Run `Invoice triage` on a sample".
2. Optional one-line scope statement above them, ≤80 chars, stating what this chat is for. No greeting.

**Follow-ups**
1. 1–3 chips, imperative fragments, ≤32 chars, ordered by likelihood: `Save as test case`, `Run 5×`, `Show the failing step`.

**Nudges**
1. One sentence: the evidence and the action. "The `Fetch` step is 71% of cost — want me to try a smaller model there?" + one chip.
2. At most one nudge per response; at most one unprompted nudge per topic per session.

## Length

Chips are fragments. A nudge is one sentence. A scope line is one sentence.

## Tone

Inherits the primary type's situation. Chips have no tone — they're labels.

## Rules

1. Every chip is something the user could have typed. Reading it tells you exactly what will happen. Follow-ups and nudges ≤32 chars; starters ≤48.
2. Follow-up and nudge chips are imperative fragments: verb first. `Save as test case`, not `Test case saving`, not `Would you like to save this?`. Starters are complete requests in the user's voice and may be questions: `Why did Invoice triage fail this morning?`.
3. Never `Learn more`, `Tell me more`, `Help`, `Other`, `Explore`, `See options`. Name the thing.
4. Prose carries the diagnosis, consequence, or result; chips carry the actions. Prose may name options when the reasoning needs them, but never as a question or offer a chip then repeats ("Want me to X?" + `[X]`).
5. Never more than 3 follow-ups. If there are five useful next steps, the reply is probably too broad.
6. Follow-ups are specific to *this* reply: after a failed run, `Retry from step 2`, not `Run again`.
7. Nudges carry their evidence in the sentence. No evidence, no nudge.
8. A dismissed nudge doesn't return in the same session. A nudge acted on doesn't return until the evidence changes.
9. Starters reflect what the surface does, in the user's words, using the user's objects when they exist. "Run `Invoice triage` on a sample" beats "Try running an agent".
10. No chips after a guardrail message except the path forward. No `Retry` chip on a guardrail.
11. Chips never carry pleasantries or emoji; follow-ups and nudges never carry questions.
12. Chips that trigger consequential actions go through `confirmation.md` when tapped; the chip label is still the plain verb.

## Components

Action chips. The empty-state scope line is a text part. Starters may render as cards when they carry an object.

## Examples

### Good — starters, user has objects
> This chat runs and tests your agents.
> [Run `Invoice triage` on a sample] [Show last week's failures] [Compare v3 and v4]

Why it works: scope line, three real things with the user's objects, no greeting.

### Bad — starters
> 👋 Hi! I'm your AI assistant. I can help you with all sorts of things! Try asking me:
> [What can you do?] [Tell me about agents] [Help]

What's wrong: greeting, emoji, self-description, chips that do nothing specific.

### Good — follow-ups after a run
> (completion) Ran `Invoice triage` on the sample: routed to `AP-review`.
> [Save as test case] [Run 5×] [Show all 3 steps]

Why it works: three specific next steps that exist in the platform; each is one tap.

### Bad — follow-ups
> [Learn more] [Run again] [Other options]

What's wrong: none says what will happen.

### Good — nudge
> `Fetch CRM data` is 71% of this run's cost — the other two steps could keep `claude-sonnet` while this one tries `claude-haiku`. 
> [Try claude-haiku on Fetch]

Why it works: evidence, specific proposal, one chip.

### Bad — nudge
> 💡 Tip: Did you know you can optimize your agents to reduce cost? Check out the Optimize tab!

What's wrong: no evidence, generic, feature marketing.

### Good — none
> (completion) Added `Route by region` after `Check PO`. Not saved yet.

Why it works: no chips. "Save" is the obvious next thing and the UI already has a save button; a chip would be noise.

## Anti-patterns

- **The greeting card** — "Hi! I'm…" with generic chips.
- **The vague chip** — `Learn more`, `Other`.
- **The echo** — "Want me to X?" followed by a chip that says X.
- **The chip flood** — five or six options.
- **The tip of the day** — evidence-free nudges.
- **The nag** — the same nudge every message.

## Rubric

Checks `SU1`–`SUn` in `evals/rubrics.md` — the single source; rules here reference them, not the other way round.
