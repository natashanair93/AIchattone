# Chat responses v1.1.1 — what I need from you

1. Open `chat-responses-v1.1.1/components/chat-components.md`. It's the only file you need.
2. Replace my guessed component names with yours (the "Maps to" row on each entry).
3. Correct the slot names and character limits to match your components. `components/response.schema.json` should change in step.
4. Resolve every **[confirm]** and **[gap]**. Either point to your existing component or say you'll build one. Known gaps: run status strip, handoff card, persistent action buttons, confirmation card.
5. Answer the 10 items under "Decisions needed". Priorities:
   - Can action chips (Retry, Request access) stay visible on error replies and not auto-dismiss?
   - Can the typing indicator show real progress labels instead of generic rotating text?
   - Are slot limits truncated at render, or rejected and regenerated?
6. Flag any of your components the AI should be able to emit that aren't listed.
7. Send back your edits by [date]. I'll update the response rules to match and re-test.
