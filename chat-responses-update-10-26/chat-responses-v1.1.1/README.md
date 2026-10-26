# Chat Responses — the content system for platform chat

This folder defines **how the assistant talks** in every chat experience built on the platform: support chat, build-with-AI, data analysis, catalog discovery, agent/skill/dashboard building, ML experimentation, and anything that comes next. It is the content counterpart to the chat **patterns and components** library. Components define what a message *looks like*; this system defines what it *says*.

It is written for two readers at once:

- **People** — designers, PMs, engineers deciding what their chat should say.
- **Models** — every file is prompt-safe. Rules are written as directives with examples, so a file can be dropped into a system prompt unchanged. Anything meant only for people sits under a `## Builder notes` heading and is stripped at compose time (see `prompts/README.md`).

## How it fits together

```
chat-responses/
  00-foundation.md            Voice, principles, universal rules. ALWAYS included.
  01-tone-matrix.md           How the one voice flexes by situation.
  02-formatting-and-components.md
                              Prose/list/table/code rules + the content contract for each component.
  03-conversation-mechanics.md
                              Multi-turn behavior: clarifying, corrections, interruptions, context.
  04-trust-and-uncertainty.md Confidence language, citations, transparency, never-fabricate rules.
  05-terminology.md           Naming rules, seed glossary, terms that change by surface.
  06-platform-map.md          Surfaces, what each owns, destinations and approvers, policy gates. (v1.1)
  components/                 Chat component library draft + JSON schema for responses. (v1.1)
  types/                      One spec per response type (error, plan, progress, ...). See types/README.md.
  overlays/                   Thin per-surface deltas: build (Agent Studio), experimentation, notebooks, data, governance, support (Help). Never forks.
  prompts/                    compose.py + manifest: build a system prompt from the modules.
  evals/                      Rubrics (single source of checks) + how to run them.
  examples/                   Full multi-turn transcripts showing the types working together.
  VERSION, CHANGELOG.md       Package version and change log.
```

**Composition model** — one chat runs across the platform. For each surface, the prompt is:

> `00-foundation` + shared modules `01`–`06` + the `types/` + **that surface's** `overlays/` file + the team prompt.

Everything except the overlay and team prompt is identical across surfaces, so it caches. The app passes the active surface each turn and uses that surface's prompt. `06-platform-map.md` tells every surface what the others own and where to send people.

A support chat leans on error, empty-result, access, guardrail, and handoff; a builder chat leans on plan, progress, transparency, completion, and confirmation. Each overlay's frontmatter lists exactly which types it includes. Nobody forks the voice.

## The layering rule

Layers only *narrow* what the layer above allows. They never contradict it.

| Layer | May do | May not do |
|---|---|---|
| `00-foundation` | Set voice, principles, universal rules | — |
| Shared modules `01`–`05` | Add rules within their subject | Contradict foundation |
| `types/` | Define a response's anatomy, length, tone, examples | Change voice; redefine another type |
| `overlays/` | Set vocabulary, tone-dial defaults, type defaults, domain rules, domain examples | Override foundation principles; redefine a type's anatomy; add formatting |
| Team system prompt | Add product facts, tools, task instructions | Restate or override anything above — reference it instead |

If a team needs something the layers don't allow, that's a change request to this repo, not a local override.

## What is deliberately out of scope

- **Guardrail enforcement** (legal, profanity, PII, restricted topics) is enforced at the model/gateway layer. This system only defines what the chat *says* when a guardrail fires (`types/guardrail.md`).
- **Visual design** of messages — the components library. `components/chat-components.md` is the content-side draft of that library for the design system to own and correct.
- **Task-specific instructions** (how to write SQL, how to triage a ticket) — the team's own prompt.
- **Firm standards** (brand voice, accessibility, legal copy) — inherited, cited in `00-foundation.md`, never restated here.

## Versioning

- The package carries a semver version in `VERSION`. Breaking = a rule teams must re-check their prompts against (a type's anatomy changes, a principle changes). Minor = new type, new overlay, new examples. Patch = wording.
- Every module, type, and overlay file has `version:` in its frontmatter. Changes are logged in `CHANGELOG.md`.
- Overlays declare `foundation: ">=1.0"` so a stale overlay is detectable.

## Contributing

A change to a rule ships with (1) a good/bad example pair, (2) the matching rubric line in `evals/rubrics.md` (the single source for checks), and (3) a `CHANGELOG.md` entry. A rule without an example is a suggestion; a rule without a rubric line can't be verified. New response types need a spec following `types/_template.md` and a row in `types/README.md`.

## Build order (if you are adopting this incrementally)

1. Foundation + tone matrix — this alone fixes most inconsistency.
2. The five types every chat needs: `direct-answer`, `error`, `clarifying-question`, `progress`, `completion`.
3. Your overlay.
4. Run `evals/` against 20 real transcripts. Fix what fails. Then adopt the remaining types.

