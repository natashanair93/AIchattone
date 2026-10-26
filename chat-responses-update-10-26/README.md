# Chat responses — update 10/26

Version **1.1.1** of the Fusion chat response system: what the AI says in every chat across the platform. Replaces `chat-responses 2/` (v1.0.0), which is kept for reference.

## Start here

- **Designers:** read [`DESIGNER-ASKS.md`](DESIGNER-ASKS.md), then [`chat-responses-v1.1.1/components/chat-components.md`](chat-responses-v1.1.1/components/chat-components.md).
- **Everyone else:** [`chat-responses-v1.1.1/README.md`](chat-responses-v1.1.1/README.md) and [`CHANGELOG.md`](chat-responses-v1.1.1/CHANGELOG.md).

## Download

- [`chat-responses-update-10-26.zip`](chat-responses-update-10-26.zip) — the whole package in one file. On GitHub, open the file and choose **Download raw file**.
- Or download the whole repository: **Code → Download ZIP** on the repo's front page.

## What's in this folder

| Path | What it is |
|---|---|
| `chat-responses-v1.1.1/` | The package: foundation, shared modules, platform map, response types, six surface overlays, components draft and JSON schema, rubrics, evaluation framework, compose script |
| `chat-responses-update-10-26.zip` | The same package, zipped |
| `DESIGNER-ASKS.md` | The asks for the chat pattern library owner |
| `testing/round1-findings-v1.0.md` | What the first stress test found in v1.0 |
| `testing/retest-findings-v1.1.md` | Retest results for v1.1 and the 1.1.1 fixes |
| `testing/review-page.html` | The full review page (download and open in a browser) |
| `testing/stress-test-harness.zip` | Scenarios, prompts, every simulated response and grade, scripts to re-run |

## What changed since v1.0

One chat across the platform (per-surface prompts with a shared prefix), a platform-only scope, a platform map of destinations and approvals, new Notebooks / Model Experimentation / Governance overlays, a JSON output contract with a component draft, and fixes for the contradictions the stress test found. On 18 unseen test scenarios: 17/18 (strong model) and 18/18 (small model), vs. 15/18 for v1.0.
