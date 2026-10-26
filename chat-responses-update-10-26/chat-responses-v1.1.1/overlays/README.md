# Overlays

An overlay is the thin layer a team adds on top of the shared system for their domain. It is a **delta**, never a fork: it sets vocabulary, defaults, thresholds, and domain rules, and adds domain examples. It cannot change the voice, the principles, or a type's anatomy.

Every composed prompt includes exactly one overlay — but one chat runs across the platform. The app composes one prompt per surface (`prompts/platform.manifest.yaml`); all of them share an identical prefix (foundation, shared modules, types), and only the overlay at the end differs. Each turn, the app uses the prompt for the surface the user is on. Overlays never assume the user stays on their surface: a question about another surface is answered with the shared rules and `06-platform-map.md`.

## What an overlay may contain

| Section | Purpose | Limits |
|---|---|---|
| `Audience` | Who the users are and their expertise | Drives depth and glossing; doesn't change voice |
| `Scope` | What this chat is for, in one sentence | Used verbatim as the empty-state scope line |
| `Vocabulary` | Domain terms, glosses, and don't-says | Adds to `05-terminology.md`; never contradicts it |
| `Tone defaults` | Shift a dial in the tone matrix by one step for a stated reason | One step; must cite the situation row |
| `Type defaults` | Which types this chat uses; lower length budgets; default chips | May lower budgets; may raise only with an audience reason |
| `Thresholds` | Cost, count, and time thresholds for confirmation and plan | Required if the chat can spend or affect shared things |
| `Domain rules` | Rules specific to the domain's content | Must not contradict any layer above; each has a rubric line |
| `Transparency level` | How much raw detail a technical audience may see | Can raise the "never shown raw" bar from `04`; cannot lower fabrication rules |
| `Handoff destinations` | The named teams, queues, and surfaces this chat hands off to | Required; "support" is not a destination |
| `Examples` | Domain versions of the type examples | Follow the same good/bad format |

## What an overlay may not contain

- A new voice, persona, name, or personality.
- New response types (propose them to `types/`).
- Formatting rules (those live in `02`).
- Restatements of shared rules "for emphasis". The compose step includes them; restating causes drift. A domain rule may *reference* a shared rule to add what's domain-specific (which limits count as limits, which wording the catalog uses).
- Task instructions (how to triage a ticket, how to write SQL). Those go in the team's own prompt, after the overlay.
- Exceptions to principles. Those are conversations, not overlays.

## Frontmatter

```yaml
---
overlay: support
version: 1.0.0
foundation: ">=1.0"
types: [direct-answer, clarifying-question, error, empty-result, access-and-capability, guardrail, handoff, suggestions]
owner: <team>
---
```

`types:` is the list the compose step includes. `foundation:` pins the range this overlay was written against; the compose step warns when it's stale.

## Template

Copy `_template.md`. Fill every section; delete none — an empty `Thresholds` section for a chat that can spend money is a bug the reviewer should catch.

## Included overlays

- `support.md` — support and troubleshooting chat: the user brings a problem (an error, a stuck run, a "why did this happen") and wants it resolved.
- `build.md` — building things with AI: agents, skills, prompts, dashboards, experiments. The user is constructing and iterating; transparency and planning dominate.
- `data.md` — asking questions of data and finding things in the catalog: queries, lookups, discovery. Precision and provenance dominate.
- `experimentation.md` — training, comparing, sweeping, and registering ML models; GPU spend. (v1.1)
- `notebooks.md` — writing, explaining, debugging, and running notebook code on shared clusters. (v1.1)
- `governance.md` — model risk validation, AI use-case review, policy, classification, audit. (v1.1)

Most experiences are one of these or a close variant. Start from the nearest and change only what your audience actually needs.
