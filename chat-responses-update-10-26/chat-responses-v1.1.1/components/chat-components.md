# Chat response components — content contract for the Fusion Chat pattern library

**Draft v0.2 · for the design system owner to correct.** This covers only the **AI response elements**: the parts the model writes into each reply. Layout, history, composer, files, and session components belong to the pattern library and aren't repeated here.

It follows the pattern library's five-field format and adds two rows per component:
- **Slots** — the fields the model fills, with limits. These must match `response.schema.json` exactly.
- **Maps to** — the pattern-library component that renders it, based on the inventory shared on 26 Oct. **[confirm]** marks a guess.

## How a reply reaches the screen

```
model ──▶ response JSON { response_type, surface, parts[] } ──validate──▶ response.schema.json ──▶ pattern-library components
```

Each `part` has a `kind`. One kind maps to one component. The model writes words into slots; the components own layout, states, motion, and the response actions toolbar (feedback, retry, copy, download).

```json
{
  "response_type": "completion",
  "surface": "agent-studio",
  "parts": [
    { "kind": "text", "body": "Created `Invoice triage` with 3 steps. It's a draft and hasn't been run yet." },
    { "kind": "card", "object_type": "agent", "title": "Invoice triage", "subtitle": "Agent · v1 · draft", "ref": "agent:8f2c" },
    { "kind": "actions", "items": [ { "label": "Run with sample data", "intent": "prompt" }, { "label": "Add a test case", "intent": "prompt" } ] }
  ]
}
```

## Index

| Kind | Component (content name) | Maps to (pattern library) |
|---|---|---|
| `text` | Message text | AI response body (markdown) |
| `code` | Code / generated content block | Syntax-highlighted code block; **Code diff view** when `variant: diff` |
| `card` | Object card | Metadata list / knowledge-base attachment card **[confirm entity card]** |
| `status` | Run status strip | **[gap — no equivalent seen]** |
| `steps` | Step list / trace summary | Accordion, nested-with-status-icons |
| `plan` | Plan card | **SummaryCard** (plan confirm/cancel) |
| `progress` | Progress label | **Typing indicator** with rotating status text |
| `evidence` | Evidence / sources | Accordion, sources/citations |
| `disclosure` | Collapsed section | Accordion, simple |
| `confirm` | Confirmation card | **SummaryCard** variant **[confirm — or a dedicated confirm card]** |
| `system` | System message | **[confirm]** system & session components |
| `input` | Input request | **ChoiceCards / SelectableCardGroup** |
| `handoff` | Handoff card | **[gap — no equivalent seen]** |
| `candidates` | Alternative answers | **Answer comparison cards** |
| `actions` | Next-step chips | **Suggested follow-ups** (prompt pills) for `intent: prompt`; **[gap]** persistent action buttons for `intent: action` |
| `starters` | Starter prompts + scope line | **Empty / new chat state** quick-start chips |
| `divider` | Thread divider | **System event divider** (as used for mode changes) |

---

### `text` — Message text
| | |
|---|---|
| **Description** | The prose of the reply. Every response that has prose opens with a text part carrying the lead sentence. |
| **When to use** | Always, except progress-only updates, starters-only empty states, and confirmations whose card leads. |
| **vs. alternatives** | Anything the user will copy or apply goes in `code`, not text. Specific objects go in `card`s. |
| **Implementation rules** | Markdown subset: paragraphs, bullet and numbered lists (≤2 levels), tables (≤5 columns, header row), `inline code`, one **bold** phrase, links with descriptive labels. No HTML, images, or horizontal rules. Headings only over ~150 words. |
| **Slots** | `body` (string) — within the response type's word budget |
| **Maps to** | AI response body |

### `code` — Code / generated content block
| | |
|---|---|
| **Description** | Code, SQL, a prompt draft, a config snippet, or a message draft the user will copy, insert, or apply. |
| **When to use** | Whenever the deliverable is text the user takes and uses. For proposed edits to existing code, use `variant: diff`. |
| **vs. alternatives** | Not for identifiers in a sentence (those are inline code in `text`). Diff only when there's a before and after. |
| **Implementation rules** | `applied` stays `false` until a tool confirms the insert or apply; the renderer shows a "Not applied" state. Collapsed over ~20 lines, with `title` and line count as the summary. Copy / Insert / Apply are renderer buttons and never also appear as chips. Doesn't count toward any prose budget. |
| **Slots** | `language`; `title` ≤60; `code`; `applied` (bool); `target` ≤60 (`new cell`, `step Write summary`); `variant`: `block` (default) / `diff` |
| **Maps to** | Syntax-highlighted code block; Code diff view |

### `card` — Object card
| | |
|---|---|
| **Description** | A compact preview of a platform object the reply refers to, which the user can open. |
| **When to use** | Whenever the reply names a specific object the user can open: an agent, dataset, model version, ticket, policy, finding. |
| **vs. alternatives** | The card is the reference; prose doesn't repeat its metadata. Use `evidence` when the point is "where a claim came from", not "here's an object". |
| **Implementation rules** | `title` is the object's exact name. `ref` only when a real ID is in context. Max ~5 cards per reply; more goes behind "Show all". |
| **Slots** | `object_type` (enum: `agent`, `agent_version`, `run`, `test_suite`, `skill`, `tool`, `mcp_server`, `knowledge_source`, `dataset`, `query`, `notebook`, `cluster`, `experiment`, `training_run`, `sweep`, `model`, `model_version`, `validation`, `use_case`, `policy`, `finding`, `access_request`, `ticket`, `incident`, `dashboard`, `workspace`, `other`); `title` ≤60; `subtitle` ≤60 (`Agent · v3 · published`); `summary` ≤120; `ref` |
| **Maps to** | Metadata list / KB attachment card **[confirm whether an entity card exists]** |

### `status` — Run status strip
| | |
|---|---|
| **Description** | Outcome at a glance for something that ran: verdict, duration, cost, eval scores. |
| **When to use** | Only on replies about something that ran: an agent run, suite, query, training run, cell. |
| **vs. alternatives** | Never on access, guardrail, approval, handoff, incident, or how-to replies. (In the v1.0 test, models added "Failed" strips to access messages.) |
| **Implementation rules** | Verdict as text, not color alone. A grading failure is `couldn't grade`, never a low score. |
| **Slots** | `verdict`: `ran_ok` / `failed` / `stopped` / `partial`; `detail` ≤40 when not ok; `metrics` ≤5 × {`label`, `value`} |
| **Maps to** | **[gap]** — propose a strip attached under the response body, beside the response actions toolbar |

### `steps` — Step list / trace summary
| | |
|---|---|
| **Description** | One line per step of a run, with outcome. Passing steps collapsed, anything not ok expanded. |
| **When to use** | A run touched ≥2 steps, or the user asked what happened. |
| **vs. alternatives** | Not a narrative. For a single step, a sentence in `text`. |
| **Implementation rules** | Step names match the canvas exactly. Every step is drillable (renderer). Steps that acted on the user's behalf are always expanded. |
| **Slots** | `summary` ≤80; `items` × {`name`, `outcome` (`ok`/`failed`/`skipped`/`stopped`), `summary` ≤80, `duration`, `cost`, `expanded`, `ref`} |
| **Maps to** | Accordion, nested-with-status-icons |

### `plan` — Plan card
| | |
|---|---|
| **Description** | What the assistant will do before doing it, with cost and consequence. |
| **When to use** | Work of ≥3 steps, >30s, touching shared resources, or costing money. |
| **vs. alternatives** | When the whole point is approving one consequential action, use `confirm`. A cost-triggered plan *is* the confirmation: its outcome carries cost and irreversibility. |
| **Implementation rules** | 3–7 steps, each checkable and ≤80 characters. Unknown time or cost is written `unknown`, never guessed. Nothing starts until the user acts when the trigger was cost or a shared effect. |
| **Slots** | `title` ≤60; `outcome` ≤160; `steps` 3–7 × ≤80; `assumptions` ≤3; `estimate` {`time`, `cost`}; `actions` × {`label` ≤40, `role`: `primary`/`alternative`/`cancel`} |
| **Maps to** | **SummaryCard** (plan confirm/cancel) |

### `progress` — Progress label
| | |
|---|---|
| **Description** | What is happening right now, replaced in place. |
| **When to use** | Any operation over ~2 seconds. |
| **vs. alternatives** | Never reports a failure; it's replaced by `system` or an error reply. |
| **Implementation rules** | The typing indicator's **rotating status text must come from these labels**: verb + exact object ("Querying `trades_emea`"), never filler ("Thinking…", "Almost there"). No percentages the platform didn't give. |
| **Slots** | `label` ≤60; `estimate` ≤30; `stop_point` ≤40 |
| **Maps to** | Typing indicator (block and inline) |

### `evidence` — Evidence / sources
| | |
|---|---|
| **Description** | Where a checkable claim came from. |
| **When to use** | Any claim from a document, query, run trace, log, or policy consulted in this conversation. |
| **vs. alternatives** | Not for general knowledge. Never lists something that wasn't opened. |
| **Implementation rules** | Exact source names. `as_of` on anything that can go stale. |
| **Slots** | `sources` ≤5 × {`label`, `locator`, `as_of`, `ref`} |
| **Maps to** | Accordion, sources/citations |

### `disclosure` — Collapsed section
| | |
|---|---|
| **Description** | Long or secondary content behind a summary line. |
| **When to use** | Content beyond the type's budget, or useful to some readers only. |
| **vs. alternatives** | Nothing the user needs in order to act may live only inside. |
| **Implementation rules** | The summary states what's inside and the conclusion (`All 5 passing steps`), never "More" or "Details". |
| **Slots** | `summary` ≤80; `parts` (nested `text`, `code`, `steps`, `evidence`) |
| **Maps to** | Accordion, simple |

### `confirm` — Confirmation card
| | |
|---|---|
| **Description** | Blocks a consequential action until the user approves it. |
| **When to use** | Destructive, irreversible, costly above threshold, shared, or affecting other people — including side effects inside user-written code (a cell that overwrites a shared table). |
| **vs. alternatives** | Not for information (that's `input`). Not for reversible local actions (just do them). |
| **Implementation rules** | The consequence leads. The primary button's label is the consequence's verb (`Overwrite table`, `Publish v4`, `Spend ~$64`), never OK / Yes / Confirm. Cancel is always present and never styled as the mistake. A safer alternative appears as a peer button. After confirm or cancel, a toast or one-line reply states what happened. |
| **Slots** | `consequence` ≤200; `reversible`: `yes`/`no`/`unknown`; `scope` ≤160; `cost` ≤30; `actions` 2–4 × {`label` ≤40, `role`: `primary`/`alternative`/`cancel`} |
| **Maps to** | **[confirm]** SummaryCard variant, or a dedicated confirmation card |

### `system` — System message
| | |
|---|---|
| **Description** | A platform failure or interruption, distinct from conversation. |
| **When to use** | A run fails or stops, or the session is interrupted. |
| **vs. alternatives** | Not for guardrails, access limits, or approval gates — those are conversation, not failures. |
| **Implementation rules** | Headline says what failed, where. At least one action, the likeliest fix first. Raw codes only in parentheses after a plain cause. |
| **Slots** | `headline` ≤80; `cause` ≤160; `actions` ≥1 × {`label`, `role`} |
| **Maps to** | **[confirm]** system & session components |

### `input` — Input request
| | |
|---|---|
| **Description** | One question with a small set of answers. |
| **When to use** | The ambiguity changes the outcome and a wrong guess is costly. |
| **vs. alternatives** | One question per message. A multi-field form (**RequirementsCard**) is only for scripted guided workflows the product runs, never improvised by the model. |
| **Implementation rules** | 2–4 options, recommended first and marked. Free text always allowed. |
| **Slots** | `question` ≤120; `options` 2–4 × {`label` ≤40, `recommended`} |
| **Maps to** | ChoiceCards / SelectableCardGroup (single-select) |

### `handoff` — Handoff card
| | |
|---|---|
| **Description** | Passes the case to a team, another surface, or an approver, with what travels. |
| **When to use** | A person, surface, or policy approval is the right next step. |
| **vs. alternatives** | Not a bare link. Not "contact support". |
| **Implementation rules** | `status: offered` until a tool confirms it was sent; only then `sent`. Destinations come from the platform map. If nothing travels, `bring` says what to bring. |
| **Slots** | `to` ≤60; `handoff_kind`: `team`/`surface`/`approval`; `status`: `offered`/`sent`; `context_sent` ≤5; `bring` ≤3; `eta` ≤40; `action` {`label`, `role`} |
| **Maps to** | **[gap]** — propose deriving from SummaryCard |

### `candidates` — Alternative answers
| | |
|---|---|
| **Description** | 2–5 alternatives the user chooses between: prompt drafts, query variants, plan options. |
| **When to use** | The user asked for options, or the right answer genuinely depends on a preference only the user holds. |
| **vs. alternatives** | Not for hedging. If one option is clearly best, recommend it in `text` and offer the other as an alternative action. |
| **Implementation rules** | Each candidate has a short title and states the deciding difference. At most one is `recommended`. |
| **Slots** | `items` 2–5 × {`title` ≤60, `body`, `recommended`} |
| **Maps to** | Answer comparison cards (grid for 2–3, carousel for 4+) |

### `actions` — Next-step chips
| | |
|---|---|
| **Description** | 1–3 tappable next steps beneath a reply. |
| **When to use** | There is a clear, useful next step the user might not know is one tap away. Never as decoration. |
| **vs. alternatives** | `intent: prompt` sends the label as the user's next message → **Suggested follow-ups** pills. `intent: action` triggers a platform action (Retry from step 2, Request access, Open in Dashboards) → needs a persistent button. |
| **Implementation rules** | Verb-first, ≤32 characters, something the user could have typed. Never a question; never repeats a prose offer. **Action chips must not auto-dismiss and must show on error replies**, because they are often the only way forward (see decisions below). |
| **Slots** | `items` 1–3 × {`label` ≤40, `intent`: `prompt`/`action`} |
| **Maps to** | Suggested follow-ups (prompts); **[gap]** persistent action buttons |

### `starters` — Starter prompts
| | |
|---|---|
| **Description** | Scope line and quick-start chips in the empty state. |
| **When to use** | New chat, before the first message. |
| **vs. alternatives** | Never mid-conversation. |
| **Implementation rules** | No greeting. 2–4 chips, using the user's real objects when they exist. Removed when the user starts typing. |
| **Slots** | `scope_line` ≤80; `items` 2–4 × {`label` ≤48} |
| **Maps to** | Empty / new chat state |

### `divider` — Thread divider
| | |
|---|---|
| **Description** | Marks a change in the thread: version, surface, or mode. |
| **When to use** | Once per change, only when the thread would otherwise be confusing. |
| **vs. alternatives** | Never on every message. |
| **Implementation rules** | Short noun phrase stating the new state. |
| **Slots** | `label` ≤40 (`Now testing v4`, `Switched to Model Experimentation`) |
| **Maps to** | System event divider |

---

## Parts each response type may use

| Response type | Expected | Also allowed | Never |
|---|---|---|---|
| direct-answer | text | code, card, evidence, disclosure, candidates, actions, divider | status, confirm, system |
| clarifying-question | text, input | card | everything else |
| plan | plan | text, card, input | status, confirm |
| progress | progress | steps | everything else |
| transparency | text, steps | status, evidence, disclosure, actions | confirm |
| completion | text | code, card, status, steps, evidence, disclosure, actions, divider | confirm, system |
| error | text; `system` for platform failures | code, status, steps, evidence, input, actions | confirm |
| empty-result | text | card, evidence, input, actions | status, system |
| confirmation | confirm | text, code, card | status, actions |
| guardrail | text | handoff, actions (path only) | status, system, input |
| access-and-capability | text | card, evidence, handoff, actions | status, system |
| handoff | handoff | text, card, confirm (approval-required), actions | status, system |
| suggestions | actions or starters | — | — |

## Where the pattern library and the response rules meet — decisions needed

1. **Suggested follow-ups auto-dismiss after 10 seconds and are hidden when the reply is an error.** The response rules require every failure, limit, and empty result to end with a way forward, usually a chip (`Retry from step 2`, `Request access`). Proposal: pills keep their behavior for `intent: prompt`; `intent: action` renders as persistent buttons that show on errors and never auto-dismiss.
2. **Typing indicator rotating text.** Generic text ("Thinking…", "Working on it…") breaks the progress rules. Proposal: the indicator shows the current `progress.label` ("Querying `trades_emea`"), with a single static fallback when there isn't one.
3. **"Mode" means two things.** The library's mode is Chat / Code / Spec. The response rules used "mode" for reading a message as a change to an agent or as an input to run. The response rules now call theirs "change vs. input".
4. **Slash commands and Test Mode settle intent.** `/test @agent` opens an isolated Test Mode thread where every message is an input; `/build`, `/fix`, `/explain` state intent outright. The response rules now treat these as explicit: no clarifying question when a slash command or Test Mode already answers it.
5. **Gaps the content rules need:** a run status strip, a handoff card, persistent action buttons, and a confirmation card (or a SummaryCard variant with consequence-first copy and verb-labeled buttons).
6. **RequirementsCard** (multi-question form) conflicts with "one question per message" unless it's part of a scripted guided workflow. Proposal: the model never emits it on its own; the product's guided workflows can.
7. **Response actions toolbar** already covers feedback, retry, copy, download, which fits the rule against asking for feedback in prose. Toolbar "Retry" regenerates the reply; a `Retry from step 2` chip re-runs an agent. Keep the labels distinct.
8. **AI-generated gradient styling** on pills and summary cards is a design call. The one content view: `confirm` cards shouldn't look celebratory.
9. Are slot limits enforced at render (truncate) or at validation (regenerate)?
10. Evidence: inline numbered pills, the sources accordion, or both?
