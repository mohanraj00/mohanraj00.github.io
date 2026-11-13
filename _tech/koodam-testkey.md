---
title: "Koodam v0.4.0-alpha.1: a gateway key for each test"
date: 2026-11-13
image: /assets/heroes/koodam-testkey.png
brand: koodam
description: "Every agent test called the model with the same key. I knew the total spend, never which test spent it. Koodam v0.4.0-alpha.1 gives each test its own short-lived gateway key, revokes it first and counts the spend after."
---

When an agent runs a test suite, every test calls the model with the same key. At the end I know the total. I don't know which test spent it, and I can't stop one bad test without stopping all of them.

[Koodam](/tech/introducing-koodam/) v0.4.0-alpha.1 fixes that with a new resource: the TestKey.

## One test, one key

A TestKey asks the controller for one short-lived gateway key, for one test in a Workspace. It has its own budget and its own TTL:

```yaml
apiVersion: core.koodam.dev/v1alpha1
kind: TestKey
metadata:
  name: login-flow
spec:
  workspaceRef:
    name: main
    uid: <the Workspace UID>
  testID: login-flow
  budget: "0.50"
  ttl: 15m
```

The budget is in the currency of the gateway price table. With the default LiteLLM prices, that is USD, so this test gets 50 cents.

The Workspace opts in with `spec.testKeys`, and sets a ceiling: `maxBudget` and `maxTTL`. A TestKey above the ceiling gets no key. The UID in `workspaceRef` must match, so a new Workspace with the same name does not inherit an old key.

## The key appears in the pod

The controller writes the key into a read-only slot in the Workspace pod, at `/etc/koodam/test-gateway/`: `key`, `alias`, `base-url` and `model`. The test reads four files. It doesn't call the Kubernetes API, and it needs no ServiceAccount token.

The alias is `tk-<testID>-<uid8>`, so the gateway spend shows the test by name. The TestKey status never holds the key, only its alias and a hash.

## Revoke first, then count

At the end of the TTL, or when you delete the TestKey, the controller blocks the key at the gateway. Then it waits 75 s by default: the gateway auth cache TTL plus a margin. Only then does it read the spend. If the key still shows as live, it blocks again. The result goes into `status.usage`: spend, calls, failed calls and tokens.

Revoke first matters. If you read the spend before the block, a test can keep calling after the count.

## What it doesn't do yet

- **One model per key.** The key permits only the Workspace model. A test that calls an OpenAI model and an Anthropic model needs a second key, and a TestKey can't give one yet.
- **Gateway calls only.** A call to an API outside the gateway, for example a decision API, still uses your own credential. Koodam doesn't count or revoke it for each test.
- **Spend, not isolation.** A TestKey splits the spend by test. It doesn't isolate one test from another: all processes in a Workspace share one trust boundary.

Next, one key will permit a list of models, so one test can use two providers ([koodam#295](https://github.com/mohanraj00/koodam/issues/295)). Keys for APIs outside the gateway wait for a real test that needs them, because the spend count works only through the gateway price table.

## The end-to-end test

Koodam's end-to-end suite runs it on a real cluster. It gives a Workspace a TestKey, reads the four files in the pod, and makes a model call with the key. After the TTL, it checks three things: the gateway blocks the key, `status.usage` counts the call, and the key files are gone.

The same Workspace also gets a folder for Nookku tests (`NOOKKU_TESTS_DIR`). [Nookku](/tech/introducing-nookku/) tests agents against their spec. Next, Nookku will use a TestKey for each of its own tests ([nookku#585](https://github.com/mohanraj00/nookku/issues/585)).

## Next: a first, small App

The Agent runs one task and ends. The next resource is an App: an agent that stays up as a Deployment behind a Service. It is not a TestKey. The App gets its own gateway key with the same revoke-first rule, a scoped Role and traced egress. Later, versions get Gateway API `HTTPRoute` weights for a traffic split.

The App work waits on one design choice, the admission approach, so I give no date. The work is in [koodam#114](https://github.com/mohanraj00/koodam/issues/114) and [koodam#183](https://github.com/mohanraj00/koodam/issues/183).

## Try it

v0.4.0-alpha.1 is a [pre-release](https://github.com/mohanraj00/koodam/releases/tag/v0.4.0-alpha.1). The API is `v1alpha1` and can change. The stable release is still v0.3.0. TestKeys need the bundled gateway (`gateway.mode: bundled`).

- [Changelog](https://github.com/mohanraj00/koodam/blob/main/CHANGELOG.md)
- [TestKey guide](https://github.com/mohanraj00/koodam/blob/main/docs/test-keys.md)
- [Code](https://github.com/mohanraj00/koodam)

If you run agent tests on Kubernetes, tell me how you count their spend today.
