# Composing a system prompt

The modules in this repo are written to be included in a system prompt as-is. This folder describes how to assemble them, in what order, and what to strip.

## The recipe

```
[00-foundation]                      always
[01..06 shared modules]              all of them for a platform-wide chat (06 is required)
[types/<each type in overlay.types>] in the order listed in types/README.md
[overlays/<surface overlay>]         the one for the surface the user is on
[team prompt]                        product facts, tools, task instructions — the team's own file
```

Foundation first, overlay last among the shared material, team prompt after everything. Order matters: a model weights later instructions more heavily on conflict, and the layering rule (`README.md`) says later layers only narrow earlier ones — so a team prompt that contradicts foundation is a bug for the reviewer to catch (the compose step concatenates; it doesn't read), not something the order should resolve.

### Which shared modules a type needs

| Type | Needs |
|---|---|
| direct-answer | 02, 04 |
| clarifying-question | 03 |
| plan | 02, 03 |
| progress | 02 |
| transparency | 02, 04 |
| completion | 02 |
| error | 02, 04 |
| empty-result | 02 |
| confirmation | 02 |
| guardrail | — |
| access-and-capability | 02 |
| handoff | 02 |
| suggestions | 02 |

`01-tone-matrix` and `05-terminology` are recommended for every composition. Include `01` whenever the chat handles more than one situation (which is always); include `05` whenever the chat names platform objects (which is nearly always).

## One chat across the platform

`platform.manifest.yaml` lists `overlays:` instead of one `overlay:` and writes one prompt per surface. Everything before the overlay is byte-identical across outputs, so cache it once. Each turn the app:
1. Knows which surface the user is on, and picks that surface's prompt.
2. Passes the active surface in the turn context (for example `surface: experimentation`), so the chat can use the right vocabulary and mark a switch.
3. Supplies tool results (runs, catalog, entitlements, policies) as tool output, not inside the user message.

`compose.py` lints every output and fails if the output contract (`02` Part C), the scope (`00`), or the destinations (`06`) are missing.

## What to strip

Every file may contain a `## Builder notes` section. It's for people. Strip it — and everything under it to the next `## ` heading or end of file — at compose time. Also strip:

- YAML frontmatter (keep it in the manifest instead).
- The `## Rubric` pointer in each type — it's for graders.
- `## Anti-patterns` — optional. They mostly restate the rules and bad examples; strip them when tokens matter, keep them when a chat has a history of a specific failure mode.

Keep everything else, including examples — they do more work than the rules.

## The manifest

A manifest declares what a team's prompt is made of, so it can be rebuilt when the package updates and diffed when it changes. See `manifest.example.yaml`.

```yaml
name: support-chat
package: chat-responses@1.0.0
overlay: support
modules: [00, 01, 02, 03, 04, 05]        # prefixes resolve to the files
types: [direct-answer, clarifying-question, plan, progress, transparency, completion, error, empty-result, confirmation, access-and-capability, guardrail, handoff, suggestions]
team_prompt: ./support-team-prompt.md
strip: [builder-notes, frontmatter, rubric, anti-patterns]
```

`compose.py` (standard library only) reads the manifest, concatenates in order, strips, warns on a stale overlay pin, and writes one file:

```
python prompts/compose.py prompts/manifest.example.yaml
```

Teams check the manifest in; the composed prompt is a build artifact (`prompts/build/` is git-ignored).

## Token budget

Rough sizes at v1.0 (after stripping), so teams can budget:

| Piece | ~Tokens |
|---|---|
| 00-foundation | 1,700 |
| 01-tone-matrix | 1,300 |
| 02-formatting-and-components | 2,100 |
| 03-conversation-mechanics | 1,500 |
| 04-trust-and-uncertainty | 1,600 |
| 05-terminology | 1,600 |
| 06-platform-map | 1,100 |
| each type | 950–1,500 |
| each overlay | 1,700–2,000 |

A full surface composition at v1.1 (foundation + 6 shared + 13 types + overlay) is roughly 30k tokens, of which about 28k is the shared, cacheable prefix (measured by `compose.py`). That's affordable with prompt caching and cheaper than the inconsistency it prevents; if it's too much for a surface, cut *types the chat doesn't use*, never foundation. The build-order list in `README.md` is the minimal set: foundation + tone + five types ≈ 9k. Examples are the bulk of every file; if a surface is token-constrained, trim the examples in the types it uses least before cutting rules.

## Rules for the team prompt

The team prompt sits after the composed modules and contains what only that team knows: product facts, available tools, task instructions, domain knowledge, examples of their specific tasks. It must not:

- Restate any rule from the modules. If a rule needs emphasis, it needs a better example in the module, not a copy in the team prompt.
- Override voice, principles, or type anatomy. If it needs to, that's a change request.
- Add a persona, name, or personality.
- Introduce terms that conflict with `05` or the overlay's vocabulary.

A short header in the team prompt should say: "The response rules above are authoritative. The instructions below describe the task and the tools; where they seem to conflict with the response rules, follow the response rules and flag the conflict." This is the model-facing version of the layering rule.

## Testing a composition

Before shipping a composed prompt:

1. Run the smoke eval in `evals/README.md` (the full eval on a first release).
2. Check the five most common situations for the chat by hand against the tone matrix.
3. Diff the composed file against the previous build; every changed line should trace to a package version bump or a team-prompt change.
