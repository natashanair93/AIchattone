# Examples

Full transcripts showing the types working together across a conversation. Single-response examples live inside each type spec; these show the *chaining* — how a plan becomes progress becomes completion, how an error becomes a handoff, how mode shifts in one thread.

Each transcript annotates every assistant turn with its type(s) in brackets, so it doubles as a worked answer key for `evals/`.

- `support-transcript.md` — a pasted error, diagnosis, a workaround, a handoff. Overlay: support.
- `build-transcript.md` — build an agent from a description, interleaved change and test messages, a stop at a limit, pushback, publish. Overlay: build.

Adding a transcript: use a real (anonymized) conversation where possible, annotate the types, and note any turn that *fails* a rubric line with the fix — a transcript with one deliberate failure teaches more than a perfect one.
