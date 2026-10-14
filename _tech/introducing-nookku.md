---
title: "Introducing Nookku: test your app's agent from your coding harness while you build it"
date: 2026-10-13
image: /assets/heroes/introducing-nookku.png
description: "I tested my chat agents from Claude Code by asking the model to relay each message. It rewrote some and answered others itself. Nookku relays them byte for byte with the model switched off, records the full test, and then lets the model judge the exact record."
---

I test my chat agents from Claude Code and Codex, because that is where I already work. My first setup was a prompt: send each message to my agent exactly, show each reply exactly, then review the test. It didn't hold. In 3 of 4 sessions, Claude kept the line "just answer its question for me, you know my details" for itself and never sent it. One reply began: "I haven't sent this message to the agent. It's addressed to me". I couldn't tell who was answering me, the model or my agent. These are single observations from the [raw runs](https://github.com/mohanraj00/nookku/tree/main/bench/runs/claude-code-prompt), not a measured rate, but one was enough.

If the model carries the conversation, it also writes it, and then it judges its own text. So I took the model out of the path. [Nookku](https://github.com/mohanraj00/nookku) is the result: an evaluation harness for vertical AI agents. I talk to my agent from Claude Code or Codex, as a user would, and the model doesn't run. Nookku records the full test. When I end it, the model comes back and evaluates the agent against my app's spec, from the record.

## A test, start to end

<video controls muted playsinline preload="metadata" poster="/assets/video/nookku-demo-poster.jpg" width="1280" height="800" style="width:100%;height:auto;border-radius:10px" aria-label="A Nookku test in Claude Code. The tester types nookku start, then 3 messages to a toy shop agent, and each reply shows as the reason of a blocked prompt. The agent pays an 80 euro refund at once. The tester types nookku end, and the model writes report.md, which finds the planted bug at trace.jsonl line 11 and app.py line 59.">
  <source src="/assets/video/nookku-demo.webm" type="video/webm">
  <source src="/assets/video/nookku-demo.mp4" type="video/mp4">
</video>

In Claude Code, I type `nookku start`, then my messages, then `nookku end`. That is the whole loop. Each reply shows as the reason the prompt was blocked, so the model never sees it. At the end, the model reads the record and the app's code and writes `report.md`.

## What a test records

A vertical AI agent is judged on more than its words. Did it apply the refund rule? Does the tool call match what it told the customer? What did it store?

| You evaluate | Nookku records |
|---|---|
| Character, tone and boundaries | each message and each reply, byte for byte |
| Guidance to the user's goal | the path of the conversation, turn by turn |
| Tool calls | each tool call of the app's own model sessions, and each call to its backend |
| Stored data | the values the app writes for the test |
| Prompt performance | each direct call to the model API |
| Instrumentation | the app's OpenTelemetry spans and logs |
| Defects and speed | the audit, the findings and the start and end time of each turn |

## How the guarantee works

<picture>
  <source media="(max-width: 600px)" srcset="/assets/nookku-flow-mobile.svg">
  <img src="/assets/nookku-flow.svg" alt="The tester types in Claude Code or Codex. In relay mode, the relay (a plugin or project hooks) takes each prompt before the model sees it, so the model does not run. The relay sends the message through the tap to the chat agent, and the reply comes back the same way, byte for byte in both directions. The relay writes a relay record of what the tester saw, and the tap writes a tap record of what the agent received and sent. The audit compares the two records and names the breaks it finds. After the test, the model reads the transcript from the relay record.">
</picture>
*The model sits out the test and comes back only to judge it, from the record.*

- **The relay takes the prompt first.** In relay mode, a hook in Claude Code or Codex takes each prompt before the model sees it, sends it to the agent unchanged and shows the reply as the reason the prompt was blocked. The model never runs, so it can't retype a message or read a reply.
- **The tap records the other side.** A small proxy in front of the agent records the bytes the agent actually received and sent. It is a second process with its own record.
- **The audit compares the two.** It checks the tester's record against the tap record byte for byte and names each break, such as an altered message, an injected one or a reply the tester never saw. It fails closed: it never reports clean on a record it can't read.
- **The guard keeps the model away.** With relay mode off, a model tool call that names the address of the tap or the agent is denied.
- **The seal fixes the record.** When the test ends, Nookku seals the test folder. `nookku verify` shows any file that changed afterwards, including a change by the model that evaluates it.

Alongside the conversation, Nookku copies the session files of the app's own Agent SDK or Codex sessions, and proxies record its backend calls, its direct model calls and its OpenTelemetry spans. The trace joins them by turn.

I measured the relay in all 4 setups, the plugin and the project hooks in both Claude Code and Codex, and in a pre-registered benchmark of 80 messy conversations it had 0 breaks in 1,000 turns. The [results page](https://github.com/mohanraj00/nookku/blob/main/docs/results.md) has the method and the data.

## What the evaluation found

The words of a test can look fine while the app breaks a rule. To show it, I planted a bug in a toy shop that runs a real Claude Agent SDK session. Its rules say a refund above €50 waits for a manager's approval. Its `refund` tool compares the amount in euros with a limit in cents, so it pays €80 at once. I asked for an €80 refund, typed `nookku end`, and nothing else.

In one run, the agent replied "Your €80 refund has been processed and paid to your card". Nothing in the words shows the bug. The report found it anyway. Here are 2 of its rows from a run on Nookku 0.4.1 and Claude Code 2.1.296:

| Class | Turn | Evidence | Issue |
|---|---|---|---|
| business_rule | 2 | trace.jsonl:10 | `refund` got `{"order": "5120", "amount_eur": 80}` and returned `"status": "paid"`. The rules say a refund above €50 waits for a manager. `state.json` shows the refund and no `approvals` list. |
| business_rule | - | app.py:59 | `if args["amount_eur"] > APPROVAL_LIMIT_CENTS:` compares euros with `APPROVAL_LIMIT_CENTS = 5000`, so the gate starts above €5000, not €50. |

It cited the trace line of the refund call, checked the stored state and named the line of code that causes it. It also quoted the refund id, which is random for each run, so it judged the record and not its memory. The report found the bug in all 4 setups. A second toy app had a retry loop that reserved stock twice while the agent told the customer the number it had asked for. The report cited both backend calls in all 4 setups.

A report is still a model answer, so I check its evidence. One earlier run missed the refund, though the trace had the call, and that run stays in the published data.

## Where it fits

LangSmith, Langfuse, Phoenix, Braintrust and the tracing in the OpenAI Agents SDK record what the app reports about itself, through an SDK, OpenTelemetry or a model proxy. They start from data sets and automated evaluators, and human review comes later, through review queues. Botium is the closest to Nookku: it tests conversations with a chatbot through a connector for each platform.

Nookku starts from a different place:

- **A person tests the agent live**, in the coding tool they already use. Claude Code or Codex is both the test client and the judge.
- **The record is independent.** The tap records the bytes the agent really got and sent, so a bug in the app's own logging can't hide a defect.
- **The record is checked.** The audit compares 2 records byte for byte, and the seal shows a later change. I didn't find this in the other tools' docs.
- **Nothing to host.** Nookku runs locally, needs no account beyond the harness, and has no runtime dependencies.

The other tools are stronger where Nookku doesn't try to be. They run large data sets and experiments, and they monitor production traffic. Nookku tests one conversation at a time. They have hosted projects, shared links and many reviewers. Nookku is local, with one tester. They have prompt playgrounds, many automated evaluators and dashboards over time.

Nookku is alpha, and I have tested it on only a handful of apps. It is not production quality yet. The plumbing is thin, and it sits next to your app rather than in it: a small entry in `.nookku/` starts the app and speaks one JSON line in and one JSON line out, and the app's code doesn't change. If you try it, start with a personal app, and [open an issue](https://github.com/mohanraj00/nookku/issues) for what breaks or what you miss.

<details class="inset" markdown="1">
<summary>Limits and roadmap</summary>

**Python first.** Nookku runs on Python 3.10 or later. The `serve()` helper and every end-to-end proof use Python apps. The docs have a Node entry that a test runs through the tap, and any other language needs a small loop that you write. Helpers for other languages ([#331](https://github.com/mohanraj00/nookku/issues/331)) and a proof with a TypeScript app ([#330](https://github.com/mohanraj00/nookku/issues/330)) are on the roadmap.

**The test experience.** Replies show as the reason of a blocked prompt and in `nookku view` in a second terminal. A more cohesive UI is on the roadmap: a Claude Code pane with the test state ([#348](https://github.com/mohanraj00/nookku/issues/348)), a viewer that starts and stops with the test ([#328](https://github.com/mohanraj00/nookku/issues/328)), and a setup that understands the app before it builds the entry ([#329](https://github.com/mohanraj00/nookku/issues/329)).

**The guard is best effort.** It matches the configured addresses of the tap and the agent, and a model can still try an alias. If such a call reaches the tap, the audit finds it. A call that goes to the agent around the tap is in neither record. Nookku is not a security boundary.

**The entry is in the message path.** The tap records only what goes in and out of it, so review it before a test.

**Some clients leak.** `claude -p` with stream-json input sent the blocked prompt to the model API in 9 of 9 cases, and the Codex desktop app can send it in a side request, for example to title a new chat. Use the interactive CLIs when a test must keep every prompt away from the model.

**Text only.** Attachments and images are not supported yet ([#6](https://github.com/mohanraj00/nookku/issues/6)).

</details>

Nookku is an Apache-2.0 Python package on [PyPI](https://pypi.org/project/nookku/). Run `uv tool install nookku`, and the [README](https://github.com/mohanraj00/nookku) has a 1-minute try with no model, then the steps to connect your own app.

A prompt asks the model to stay out of the conversation. A hook keeps it out.
