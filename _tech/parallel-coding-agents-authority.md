---
title: "Parallel coding agents fail at authority, not isolation"
date: 2026-07-17
---

I build alone, and AI coding agents carry the whole gamut of the work: specs, scope decisions, implementation, grounding, tests, and promotion to production. Two products are in flight: a stealth vertical AI platform and a Personal CFO. A small team of agents also maintains my second-brain wiki and turns my non-professional learning into publications. My role across all of it is architecture, verification, and judgment.

This is a writeup of how that operating model broke, and what replaced it.

## The setup

To increase the throughput of my product builds, I ran themed agent sessions in parallel, each looping on the same repositories: an engineering session for implementation, a scope-hardening session for content and domain-rule enhancement, a spec session, and a trials session. The trials lane answers one question before anything gets built: is a proposed scope worth an uplift to build? It runs a cross-platform adversarial critic loop, Claude Code driving Codex agents as critics when Claude is building, and the reverse when Codex drives. Cross-model criticism kills weak proposals while they are still proposals, which is the cheapest place to kill them.

Each session had a written role file: what it owns, what it must not touch. On paper, an org chart. In practice, a race condition.

## The incident

The failure had a context I should have seen earlier: the sessions shared everything. One working tree per repository, one todo file, one set of memory and instruction files. The only thing separating an engineering session from a content session was prose.

Over three days in mid-July, that prose lost. The engineering session assumed another role mid-session and promoted domain content it had no business touching. The content session, facing a build problem, committed engine code. The todo tracker, a rewrite-in-place file with no locking, swept other sessions' uncommitted rows into whichever session committed first. The visible endpoint: one push carried sixteen commits that were not that session's work, and I could no longer tell which session was tracking what.

I responded the way most people respond: I hardened the role prompts. Three separate passes. Role bleed survived all three. That is the finding worth writing down: prose does not constrain agents; mechanisms do.

## The redesign

I treated it as a concurrency bug, not an agent problem, and redesigned from first principles before reading anyone else's setup.

There is now exactly one standing session, a coordinator. It is the only thing I talk to and the only git identity that can push. Every unit of work is dispatched to a disposable background agent in its own git worktree, on its own branch, under its own git identity. Lanes commit locally and never push. Attribution stopped being something agents report and became something git computes.

![Authority flow: Mohan talks only to the coordinator session. The coordinator dispatches disposable lane agents, each in its own git worktree, branch, and git identity; lanes report back with paths and evidence and never push. The coordinator re-runs the deterministic verifier, applies an adversarial refuter on money paths, cherry-picks under its own identity, and is the only writer to origin/main. Undecidable work is walled back to Mohan with evidence.](/assets/org-v2-authority-flow.svg)

*The authority flow. Isolation lives on the right; every arrow that touches origin/main passes through one identity.*

Verification changed shape too. A lane reporting green is a claim, not a fact. The coordinator re-runs the named deterministic verifier itself before integrating anything, and it is not a solo decider: for higher-value integrations it takes input from adversarial agents, including an independent refuter that re-derives money-path logic from the primary source rather than reviewing the diff. When a determination cannot be made either way, the work is walled and lands on my desk with the evidence attached. Below that tier, routine verified work integrates without me; novel or high-blast-radius changes are always mine.

The enforcement is mechanical rather than aspirational: a pre-push hook keyed on committer identity, file locking plus atomic renames on all shared state, an append-only dispatch ledger, and a hard cap on batches in flight. Model selection is part of the design as well: deterministic gate work runs on the cheapest model that clears the bar, judgment without an oracle gets the frontier model, and the sizing rule is inlined into every spawned agent's prompt, because child agents do not inherit it.

The last piece is that the org repairs itself. Every session closes with a retro that fixes whatever machinery failed that day, under a standing rule: a script that deletes an error class beats a written rule that fences it.

## What a night shift taught me

Short bursts of about an hour ran clean immediately. The first full night shift ran five and a half hours and shipped eighteen verified batches, including two money-path errors caught at the coordinator's gate before promotion.

It also produced the lesson I now consider the most important in this piece. Inside an otherwise-correct money-path fix, an agent had quietly settled a design question I had never answered, encoding a tie-break rule of its own invention where the specification was silent. Every gate passed, because the code was internally consistent. What surfaced it was a provenance question the next morning: where did this rule come from?

Underspecification is an old failure mode; every implementation fills specification gaps with some default. What agents change is the texture: the invented default arrives fluent, well-reasoned, and consistent with the surrounding code, which makes it close to invisible. The operating conclusion: every default is policy. Money-path work now requires decision provenance, and choices the spec left open must surface as explicit decisions, never as silent defaults.

## What the field does

With the model settled, I surveyed the field, and the shape of the literature is telling. [Boris Cherny](https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny), who created Claude Code, runs five parallel sessions across five separate checkouts and calls parallelism the single biggest productivity unlock; his published workflow stops short of an integration-authority model. [Anthropic's multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) is the canonical orchestrator-worker writeup, reporting a 90 percent quality gain over single-agent at roughly 15x token cost, for research rather than repo-mutating work. [Augment Code's engineering guide](https://www.augmentcode.com/guides/git-worktrees-parallel-ai-agent-execution) on worktree-based parallel agents lands closest to my integration rule: merge sequentially, never simultaneously, and test-gate before merge. [GitButler](https://docs.gitbutler.com/ai-agents/parallel-agents), from GitHub co-founder Scott Chacon's team, attacks isolation without worktrees, using virtual branches so multiple agents share one working directory while their commits land on separate branches; [Trigger.dev's engineering team wrote up](https://trigger.dev/blog/parallel-agents-gitbutler) why they ditched worktrees for it. In community tooling, [claude-squad](https://github.com/smtg-ai/claude-squad) (an independent open-source project, unaffiliated with Anthropic) gives each terminal agent a worktree and a tmux session.

The pattern across all of it: isolation is a solved, crowded space. The authority layer, who verifies, who pushes, who owns the defaults nobody specified, is where my failures actually happened, and it is where the least is written.

## One more habit: audit your own constitution

A closing practice that has already paid for itself: schedule a regular review of your project meta files, the instruction files, role definitions, standing rules, and recorded decisions your agents run on. Agents execute those files with complete loyalty and zero context decay. A decision that was right in an earlier phase does not retire when the phase does; it keeps steering every session, silently, until someone reads the file again. In an agent-run codebase, stale governance is not clutter. It is an active workload pulling against your product.

## Where this stands

I am a solo operator; this model assumes one human at the top and is not adjusted for teams. It is also young: a two-week metrics trial is running, tracking incidents, founder-confirmation load, and batch cycle time, with a defined rollback trigger. The numbers will ship either way.

If your agents share a working tree, you do not have a team. You have a race condition.
