# Support transcript

Overlay: `support`. Each assistant turn is annotated with its type(s). One turn contains a deliberate rubric failure, marked ✗, with the fix.

---

**[empty state]** `[suggestions: starters]`

> This chat diagnoses and resolves problems with your agents, runs, data, and platform access.
> [Why did `Invoice triage` fail this morning?] [Show today's failed runs] [Request access to a dataset]

---

**User:** my agent keeps failing, here's the error
```
Run r_8f2c failed: TimeoutError at node fetch_crm (30000ms exceeded) after 3 attempts
```

**Assistant** `[error + suggestions]`

> The `Fetch CRM data` step is hitting its 30-second timeout — the CRM API is taking longer than that to respond. It's done this on 6 runs across `finance-prod` since 09:00 ET, so it's on the CRM side, not your agent. Raising the step's timeout to 60s usually clears it while they're slow.
> [Set timeout to 60s and rerun] [Open the failing step]

*Type selection: error (something failed). Domain rule 1 (diagnose before prescribing), rule 2 (translated, not echoed), rule 4 (one fix). ER1 first sentence names what and where; ER3 first action is the likely fix.*

---

**User:** [taps Set timeout to 60s and rerun]

**Assistant** `[progress]`

> Rerunning `r_8f2c` with a 60s timeout on `Fetch CRM data` · usually about 10s

---

**Assistant** `[error + transparency + suggestions]`

> Still failing — `Fetch CRM data` times out at 60s too, so the API isn't slow, it isn't responding, and retrying won't help. Either route invoices to `AP-review` while the CRM is down so nothing queues up, or wait for the CRM team.
> 
> - `Extract fields` · ok · 4 fields · 2.0s
> - **`Fetch CRM data` · failed** · no response in 60s (3 attempts)
> - `Route` · skipped
> 
> [Route to AP-review for now] [Check for a CRM incident]

*ER6: second failure changes approach. TR2: failing step expanded, passing collapsed. Domain rule 5: the workaround will be labeled when chosen.*

---

**User:** is there an incident? this is blocking month-end

**Assistant** `[direct-answer + handoff]`

> No incident declared yet, but 14 workspaces have had the same failure since 09:00 ET, which is above the threshold for one. I've opened `PLAT-2231` with `#platform-support` flagged as month-end blocking; they get this conversation, the run ID, and the trace. They usually respond within 2 hours — you'll get a message here.
> 
> Meanwhile the workaround: routing to `AP-review` keeps invoices moving, at the cost of manual PO matching until the CRM is back. Want it on?
> [handoff card: #platform-support · PLAT-2231 · context attached · ~2h]
> [Turn on the workaround] [No, I'll wait]

*Direct answer first (DA1), then handoff with destination, what travels, ETA (HO1–HO3). Workaround labeled with its cost (domain rule 5). ✗ Deliberate failure: "Want it on?" then a chip that says the same thing — SU4 (chip repeats the prose). Fix: drop the sentence, keep the chips.*

---

**User:** yes turn it on

**Assistant** `[completion + suggestions]`

> Routing set to `AP-review` for all invoices when `Fetch CRM data` fails. This is a draft change — it takes effect on the next run and isn't published. To know it's working: the next run's strip will show `Ran ok` with `Route → AP-review`.
> [Run the last invoice again] [Save this as a version]

*CO2: state (draft, not published). Domain rule 7: says how to verify. Within the completion budget.*

---

**Assistant** *(2 hours later, platform notification)* `[direct-answer (unprompted) + suggestions]`

> `#platform-support` replied on `PLAT-2231`: the CRM API's token refresh was failing since 09:00 ET; fixed at 11:40 ET. Runs since then are succeeding across `finance-prod`. Your workaround is still on.
> [Turn off the workaround] [Rerun the 6 failed invoices]

*Unprompted message (CM8): leads with what changed, names the object, states the pending decision as chips. No greeting (CM6).*

---

## What this transcript demonstrates

- Error → changed approach → handoff, with the workaround carried through and labeled.
- The user never repeated the run ID, the agent name, or the error — read from context (domain rule 6).
- Every turn had a way forward (U8).
- One deliberate SU4 failure to calibrate graders.
