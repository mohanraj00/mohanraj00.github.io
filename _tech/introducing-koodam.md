---
title: "Bring your Claude Code to Kubernetes, not a new agent platform"
date: 2026-10-22
image: /assets/heroes/introducing-koodam.png
description: "My Claude Code and Codex sessions outgrew my laptop. The Kubernetes agent projects I found want me to rebuild my agents for their platform. Koodam moves the setup I already have to my cluster: my subscription login, my skills, my sessions and the Claude desktop app."
---

I run several Claude Code and Codex sessions at once, each for hours. My laptop can't carry them. It stays on power all day, because a session dies when the battery does.

My setup is more than a binary: Claude Code and Codex on my own subscriptions, the desktop app for most work and the CLI for spikes, one `AGENTS.md` for both harnesses, and my skills. I wanted to move it to a cluster and change as little as possible. I also wanted to host the agents I build on Kubernetes, the platform I know best, and to develop on my subscriptions, not API keys.

## What I found

**kagent, agent-sandbox, ARK and kars host production agents.** None of them gives me an interactive Claude Code session on my subscription out of the box.

- [kagent](https://github.com/kagent-dev/kagent) runs Claude Code in print mode with an API key or Bedrock, behind its own API and UI.
- [agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox) gives isolated, stateful pods. The SSH image, the login and the skills are mine to build.
- [ARK](https://github.com/mckinsey/agents-at-scale-ark) has a Claude executor on the Agent SDK with API credentials.
- [kars](https://github.com/Azure/kars) is a governed agent reference stack for AKS. I found no Claude Code or Codex CLI workflow.

They will fit when I run my own agents at scale. I'm not there yet.

**kelos and Coder are close.** [kelos](https://github.com/kelos-dev/kelos) runs Claude Code and Codex with my login and my skills, and keeps sessions alive. I reach them through its CLI or web console, not SSH or the desktop app. [Coder](https://github.com/coder/coder) gives SSH workspaces that the desktop app lists. It is a full platform with its own server, users, login and Terraform templates, under AGPL.

I didn't want a new platform on top of my cluster. I wanted a small part that adds my setup to the cluster I already run.

## Koodam

[Koodam](https://github.com/mohanraj00/koodam) (short for தொழிற்கூடம், "workspace") is that part: a Helm chart and a CLI. The chart uses your LiteLLM gateway, or installs one with PostgreSQL.

**A Workspace holds my long-running sessions.** It is a StatefulSet pod with a home on a PVC and tmux. I connect over SSH from a terminal or the Claude desktop app. When I disconnect, the sessions keep running. If the pod restarts, the home stays and the tmux sessions don't.

```yaml
apiVersion: core.koodam.dev/v1alpha1
kind: Workspace
metadata:
  name: main
  namespace: dev
spec:
  storage: 20Gi
```

**A Profile puts my setup in every pod.** It binds namespaces. Each developer gets a namespace, their own login and their own skills:

```sh
koodam login claude-code -n dev   # one subscription login, stored in a Secret
koodam profile push -n dev        # my CLAUDE.md, AGENTS.md and skills
```

Every Workspace in that namespace gets them. `profile push` rejects known credential files and private keys.

**The pod is restricted.** It meets the Pod Security `restricted` profile and gets no ServiceAccount token. There is no public Service. `koodam tunnel` carries SSH through the Kubernetes API, so you need Kubernetes permission for the tunnel and an authorized key for SSH. Egress is still open.

**Why not a StatefulSet with sshd and tmux?** That is what a Workspace is. Koodam does the parts I got tired of doing by hand: the host key, the authorized keys, the SSH config entry, the tunnel, the namespace binding, and one login and one set of skills in every pod.

**An Agent runs one task for the agents I build.** It is a one-time Job with the same harness. Each run gets its own ServiceAccount, a Role with only the rules it asks for, and a gateway key. Koodam removes all three when the run ends.

## A day with Koodam

With a Profile bound to `dev` and the harness installed in the home:

```sh
kubectl apply -f workspace.yaml
koodam ssh setup main -n dev   # key, host entry, public key on the Workspace
```

1. I open the Claude desktop app and add the host `koodam-main.dev`. My skills and `CLAUDE.md` are there, with no login in the pod.
2. I start a few sessions and close the laptop.
3. Later I connect from the app or with `koodam ssh main -n dev`. The sessions kept running.

## Where it fits

| | Built for | Live CLI session | Subscription login | Desktop app | What you install |
|---|---|---|---|---|---|
| kagent | teams that build agents | its own API and UI | no, API key or Bedrock | none found | a controller and its resources |
| agent-sandbox | platforms that need isolated pods | you build it | you build it | you build it | a controller and CRDs |
| ARK | enterprise agent workflows | Agent SDK executor | no, API credentials | none found | a CLI, a controller, a dashboard |
| kars | governed agents on AKS | none found | none found | none found | a reference stack |
| kelos | coding agents and their tasks | yes, its CLI or console | yes | none found | a controller and a CLI |
| Coder | team dev environments | yes | yes, from the template | yes | a server, its database, templates |
| Koodam | team dev environments and agents | yes, SSH and tmux | yes, one login per namespace | yes | a Helm chart, a CLI, a LiteLLM gateway |

## Where it is now

Koodam is at [v0.2.0](https://github.com/mohanraj00/koodam/releases/tag/v0.2.0), Apache-2.0 and pre-alpha. The API will change. Each release ships the controller image, the Helm chart and the CLI for Linux and macOS. In v0.2 you install the harness CLIs in the home once, and they stay on the PVC. Koodam will handle it in the v0.3 release.

## What's next

1. **Codex at the same level as Claude Code.** The Workspace installs the harnesses from its spec, and every pod gets the Codex login ([#98](https://github.com/mohanraj00/koodam/issues/98), [#108](https://github.com/mohanraj00/koodam/issues/108)).
2. **A stronger pod.** Egress rules, and the full Kubernetes pod template for CPU and memory limits, a gVisor or Kata runtime class and placement ([#109](https://github.com/mohanraj00/koodam/issues/109), [#115](https://github.com/mohanraj00/koodam/issues/115)).
3. **A portal** for your Workspaces and runs, with metrics and usage for each Profile, that acts with the identity of the person viewing it ([#13](https://github.com/mohanraj00/koodam/issues/13)).
4. **Beyond coding sessions.** Test my agents with [Nookku](https://github.com/mohanraj00/nookku) on the cluster ([#83](https://github.com/mohanraj00/koodam/issues/83)), then host vertical AI applications that serve clients ([#114](https://github.com/mohanraj00/koodam/issues/114)).

The [Workspace guide](https://github.com/mohanraj00/koodam/blob/main/docs/workspaces.md) takes you from the chart to a desktop app session. If you run coding agents on Kubernetes, [open an issue](https://github.com/mohanraj00/koodam/issues) for what breaks or what you still wire by hand.

Keep your tools. Give them a bigger machine.
