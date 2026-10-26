---
title: "The company that forgets what it knows"
date: 2026-10-26
synapse: 23
tags: [ai, coding-agents, anthropology, mary-douglas, kodak, institutions]
image: /assets/heroes/the-company-that-forgets-what-it-knows.jpg
excerpt: "Google's coding agent forgets your project. Google's NotebookLM is built to remember your documents. An anthropologist explained this gap in 1986."
---

Google's coding agent, [Antigravity](https://en.wikipedia.org/wiki/Google_Antigravity), does not reliably remember your project. Its users report saved knowledge that [leaks into the wrong workspace](https://discuss.ai.google.dev/t/workspace-knowledge-items-exposed-in-a-new-workspace/122315), and saves that report success but [write no files](https://discuss.ai.google.dev/t/bug-persistent-context-broken-on-windows/130236). Google's [own docs](https://antigravity.google/docs/rules) say the instruction files in a project, AGENTS.md and GEMINI.md, are always on. Since June, users on Google's forum report that agents [ignore those rules anyway](https://discuss.ai.google.dev/t/bug-feedback-antigravity-2-2-1-models-not-following-global-nor-agents-rules-fake-using-skills-tools/172904). A [canary test](https://github.com/pingdotgg/t3code/issues/15283) found that one way to run the agent loads none of them. That matches my own use.

The strange part is that Google already solved this. NotebookLM, also from Google, answers only from the documents you give it, and it links each answer to the passage it came from. So Google knows how to do it. The agent is a different team's product: a VS Code fork built on licensed [Windsurf technology](https://www.thoughtworks.com/radar/tools/google-antigravity) and led by the Windsurf people that Google hired in 2025. The knowledge exists. It is in another part of the company.

## An old pattern

Big companies often know the answer and still do not use it.

In 1975, Steve Sasson at Kodak built the [first self-contained digital camera](https://spectrum.ieee.org/first-digital-camera-history). He later recalled that executives doubted anyone "would ever want to look at their pictures on a television set." Kodak was a film company.

In 2003, Microsoft had about [95% of the browser market](https://en.wikipedia.org/wiki/Internet_Explorer_6). It then waited five years between IE6 and IE7. Firefox, and later Chrome, took the market.

Xerox PARC built the graphical desktop. Xerox made money from PARC's laser printer, which fit a document company. Apple and Microsoft made money from the desktop.

It still happens. Amazon [steers its engineers to its own tool](https://www.techrepublic.com/article/news-amazon-engineers-revolt-over-ai-tool-restrictions/) and puts Claude Code behind special approval, while it sells Claude Code to AWS customers. Apple announced Swift Assist in 2024, never shipped it under that name, and in 2026 [put Claude and Codex into Xcode](https://www.apple.com/newsroom/2026/02/xcode-26-point-3-unlocks-the-power-of-agentic-coding/).

## What an anthropologist saw

The usual explanation is money: a new product threatens the old one. The anthropologist Mary Douglas gave a deeper one in *How Institutions Think* (1986). One chapter is called "Institutions Remember and Forget".

Douglas argued that an institution decides what its members can remember. It keeps the knowledge that fits its categories and lets the rest fall away. Anthropologists call this *structural amnesia*, a term usually credited to John Barnes. He saw that family trees forget the ancestors who no longer matter to how the living group is organised.

In her earlier work, Douglas called a thing that fits no category "matter out of place". A filmless camera inside a film company was matter out of place. Kodak did not lack the camera. It lacked a place to put it.

That is the best way I can explain Google's gap. NotebookLM's skill exists inside Google, but nothing makes the coding team treat it as their own. The tool forgets your project, and the company forgets what one of its own teams knows. It is the same failure at two scales.

Money cannot buy memory. An institution remembers only what it has a place for.
