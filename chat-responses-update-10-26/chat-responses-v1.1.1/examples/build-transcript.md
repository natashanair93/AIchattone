# Build transcript

Overlay: `build`. Each assistant turn is annotated with its type(s). One turn contains a deliberate rubric failure, marked ✗, with the fix.

---

**User:** I want an agent that reads vendor emails and tells me which ones need attention today

**Assistant** `[plan]`

> I'll build a three-step agent that sorts vendor emails into `Urgent`, `Routine`, and `No action`.
> 1. Extract sender, subject, deadline, and what's being asked
> 2. Classify urgency from the deadline and the ask
> 3. Route to the matching queue
> 
> Assumptions: a deadline within 48 hours means `Urgent`; emails with no ask and no deadline are `No action`. About 1 minute; nothing published.
> [Start] [Edit plan]

*PL1 outcome first; PL3 both assumptions are real forks; PL4 time and shared-effect stated.*

---

**User:** [Start]

**Assistant** `[progress]` → `[completion + suggestions]`

> Building `Vendor email triage` · step 2 of 3

> Created `Vendor email triage` with 3 steps. It's a draft and hasn't been run yet.
> [card: Vendor email triage · Agent · v1 draft]
> [Run with a sample email] [Paste a real email]

*CO2 state stated. Chips are the two ways to first-run it.*

---

**User:** [pastes an email: "Hi, the Q3 invoice is attached, please process by Friday. Thanks, Dana"]

**Assistant** `[completion + transparency + suggestions]`

> Ran it: `Urgent`, deadline read as Friday 5 Sep. Check the deadline — the email says "by Friday" without a date, and I took the coming Friday.
> 
> [status: Ran ok · 4s · $0.01]
> - `Extract` · ok · sender, subject, deadline, ask · 1.8s
> - `Classify` · ok · Urgent (deadline < 48h) · 1.9s
> - `Route` · ok · → Urgent queue · 0.3s
> [Save as test case] [Run 5×]

*Domain rule 1: read as an input, so it ran. CO3 the specific thing to check. TR2, TR3.*

---

**User:** also pull out the invoice number

**Assistant** `[completion (micro)]`

> Added `invoice number` to step 1's extracted fields. Not saved yet.
> [Rerun last input]

*Domain rule 1: read as a change; rule 2: named by step; CO2 state. Past tense because the edit tool confirmed the change (U6). The rerun is a chip, not also a prose question (SU4).*

---

**User:** make it shorter

**Assistant** `[clarifying-question]`

> Is that a change to the agent's instructions, or an email to run?
> [Change the instructions] [Run it as input]

*CQ2: ambiguous, and a misread either way is costly (an instruction triaged as an email, or an email edit lost). Domain rule 1 says ask here.*

---

**User:** change — the routing message it writes is too long

**Assistant** `[completion (micro)]`

> Shortened the routing message in step 3 to one line: queue, deadline, and the ask. Not saved yet.
> [Rerun last input] [Show the new message format]

---

**User:** ok now run it against last week's emails

**Assistant** `[plan]`

> I'll run last week's 212 emails from `vendor-inbox` through the agent and summarize the split.
> 1. Run all 212 on `claude-sonnet`
> 2. Tally Urgent / Routine / No action, and any stops
> 3. Show the ones worth checking by hand
> 
> About $2.40 and 4 minutes; results save to this agent's run history. A 20-email sample is about $0.25 and 30 seconds.
> [Run 212 · ~$2.40] [Run a sample of 20 · ~$0.25]

*Not a confirmation: $2.40 is under the $10 threshold and run history being visible to the workspace changes nothing for anyone else. It's a plan (>30s), shown with cost and the cheaper path; PL4, PL5 — it waits because the user chooses the size.*

---

**User:** [Run a sample of 20]

**Assistant** `[progress]` → `[completion (Partial) + transparency + suggestions]`

> Running 20 emails · 12 of 20 · 11 ok, 1 stopped

> 19 of 20 ran ok. One stopped: email 7 hit the 10-turn max — `Classify` kept calling `Search knowledge` for a vendor policy the knowledge source doesn't have.
> 
> - 19 emails · ok · 14 Urgent, 4 Routine, 1 No action
> - **Email 7 · stopped** · 10 turns · `Search knowledge` × 6 with the same query
> 
> [Open email 7's run] [Add a no-results fallback] [Save the 19 as test cases]

*T6: 19 of 20 usable, so this is a completion with a `Partial` verdict, not an error; the stop expands inside it. Domain rule 5: "stopped", limit named, repeated step named. ✗ Deliberate failure: "14 Urgent" of 19 sampled emails is a striking number and the response doesn't flag that the 48h assumption may be too broad — U-level judgment isn't a rubric line, but PL3's assumption should resurface as a nudge here. Fix: add one nudge with evidence: "14 of 19 came out Urgent — the 48-hour rule may be too broad. [Try 24 hours]".*

---

**User:** add the fallback and use opus everywhere, I want it accurate

**Assistant** `[completion (micro) + direct-answer (pushback) + suggestions]`

> Added a fallback to `Classify`: when `Search knowledge` returns nothing, it classifies from the email alone. Not saved yet.
> 
> On `claude-opus` everywhere: `Extract` and `Route` are mechanical — `claude-opus` there roughly triples cost with no accuracy change on the 19 runs. `Classify` is where reasoning matters. I'd put `claude-opus` on `Classify` only.
> [claude-opus on Classify only] [claude-opus everywhere]

*Domain rule 9: pushback once, with the number, then the user's option stays available. U4: no agreeing to be agreeable.*

---

**User:** fine, classify only. publish it

**Assistant** `[confirmation]`

> Publishing requires a saved version, and the draft has 4 unsaved changes. This saves them as v1 and publishes v1 to `finance-prod` — 14 people get it on their next run. You can roll back from the version list.
> [Save v1 and publish] [Cancel]

*Confirmation rule 10 (scope creep: the save step). CF2 who is affected, count. Reversibility stated.*

---

**User:** [Save v1 and publish]

**Assistant** `[completion + suggestions]`

> Published `Vendor email triage` v1 to `finance-prod`. It's live for the 14 people in the workspace on their next run.
> [card: Vendor email triage · v1 · published]
> [Set up a daily run] [Save 19 results as test cases]

*CO5 shared effect and who. No victory lap.*

---

## What this transcript demonstrates

- Plan → progress → completion → transparency chain, twice — once ending in a `Partial` completion.
- Change vs. input reading made visible on every message, and asked about once.
- Stopped ≠ failed.
- Pushback once, with a number, then the user's choice honored.
- A plan (not a confirmation) for a below-threshold run; a confirmation for publish, with the scope-creep save step explained.
- One deliberate omission (the 14/19 nudge) to calibrate graders on judgment, not just rules.
