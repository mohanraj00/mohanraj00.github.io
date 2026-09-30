---
title: "Grounding is a contract, not a citation"
date: 2026-09-29
image: /assets/heroes/grounding-is-a-contract.png
description: "Seven LLMs made 117 wrong extractions from 30 government documents. LangExtract's exact-match filter accepted 115. A deterministic value gate let 8 through."
---

I'm building a stealth vertical AI platform that extracts data from authoritative documents. The numbers it extracts end up on money paths, so the failure I guard against most is a wrong number that looks right: a confident value with a citation to a real sentence.

My pipeline already runs value checks of its own on every fact. When I evaluated [LangExtract](https://github.com/google/langextract), an open-source library published under Google's GitHub organization that promises to map "every extraction to its exact location in the source text", I wanted to know whether its grounding made those checks redundant. So I rebuilt the checks from scratch as an open-source gate, groundgate, and measured both on the same benchmark.

Seven models ran through LangExtract on 30 public-domain government documents and made 117 wrong extractions out of 4,350. Keeping only LangExtract's exact alignments, its strictest filter, let 115 of them through, each citing a real sentence in the source. groundgate let 8 through.

## What an exact match checks

LangExtract does what it promises. It finds where each extraction's quoted text sits in the source and reports how well the quote aligned. The value you store lives in the extraction's attributes, and nothing compares it with that text. Here is a planted error from the benchmark that LangExtract reports as an exact match:

```text
extraction_text:  "$8,000"
attributes:       {"value": "80000", "unit": "USD"}
alignment_status: MATCH_EXACT
```

The quote is real. The number is off by ten, and nothing downstream has a reason to doubt it, because it carries a citation. LangExtract never claims to check values. The question is whether an exact alignment is enough evidence to admit a fact into your data.

A citation is half of a contract. It says where to look. The other half says what that span has to support: this value, in this unit, with nothing next to it that changes its meaning, for the condition the field asks about. LangExtract delivers the first half. groundgate enforces the second half except the condition, and six of the eight escapes came through that gap. The other two came through the unit rule.

## A gate between the model and the dataset

An extraction pipeline asks what a document says. A pipeline that feeds a dataset or a decision also has to ask whether each fact gets in. I keep those questions in separate components for the same reason I keep [building and verifying apart for coding agents](/tech/parallel-coding-agents-authority/): the component that produces a fact never approves it. The model proposes candidates, and a deterministic gate admits each one, sends it to a person, or rejects it.

<picture>
  <source media="(max-width: 600px)" srcset="/assets/grounding-admission-gate-mobile.svg">
  <img src="/assets/grounding-admission-gate.svg" alt="A document goes to an extractor, an LLM running through LangExtract, which proposes candidate facts, each with a value, a unit and a cited span. A dashed admission boundary separates proposing from deciding. On the deciding side, groundgate runs value, unit, qualifier and conflict checks and sends each candidate to one of three outcomes: admitted into the dataset, needs verification and routed to a person with the span, or rejected with a reason code. Next to groundgate, a receipt records hashes of every input and can be re-derived by anyone.">
</picture>
*Every candidate leaves with one outcome and its reason codes, and every run leaves a receipt.*

[groundgate](https://github.com/mohanraj00/groundgate) is an Apache-2.0 Python library with no dependencies in its core. It takes the document, a schema of the fields you want, and the candidates an extractor proposed. For each candidate it checks that the cited span contains the value as a number, with the field's unit next to it. It flags a qualifier the field doesn't allow, such as "more than" in front of a value the field defines as a minimum, a scale word such as "million" after the number, and two proposals for one field that disagree. A candidate that fails a check is rejected with a stable reason code. One that trips a flag becomes `needs_verification` and goes to a person with the span to read.

It never calls a model, so the same inputs give the same decisions, and every run writes a receipt that `groundgate verify` re-derives from the inputs byte for byte. The rules live in a written [spec](https://github.com/mohanraj00/groundgate/blob/main/SPEC.md) with 107 language-neutral conformance cases, so an implementation in another language can check that it agrees. The gate is also cheap. Across all 420 benchmark documents it took 0.7 seconds on my laptop, 2.6 ms per document at the 95th percentile, against about five hours of model time.

groundgate reads LangExtract's output directly and checks each extraction's value and unit at the place LangExtract aligned it. LangExtract stays in the pipeline, because its alignment is why the evidence spans exist at all.

## How I measured it

I set the method before any model ran and scored against spec 0.1, frozen at one commit. One change came after the runs: a code fix that brought the implementation into line with that spec. It is described below, with the numbers from both sides of it.

The documents are public domain: 10 FDA drug labels (dosage and strength sections), 10 NTSB aviation accident reports, and the first two pages of 10 IRS publications. I picked them by rules written before any model ran, and excluded the two documents I used while building groundgate. Each document gets its own fields, such as starting and maximum doses, pilot hours, weather readings, contribution limits and phase-out thresholds.

Claude drafted the gold, and I checked all 277 facts and 33 absent fields in 2.4 hours, in a labeling app that never shows the benchmarked models' output. Tables were the slowest part. PDF text flattens an IRS table into row labels followed by values, so the app links each document to its original page. The models read the same flattened text.

Each model ran through LangExtract at its default chunk size of 1,000 characters and again at 4,000, for 14 runs: Gemini 3.6 Flash and Gemini 3.8 Flash through the Antigravity CLI, GPT-5.6 Luna and GPT-5.6 Terra through Codex, and Claude Sonnet 5.5, Haiku 4.5 and Sonnet 4.6 through Claude Code. Every raw reply is cached, so CI rebuilds every score with no API key.

## What the gate caught

<picture>
  <source media="(max-width: 600px)" srcset="/assets/grounding-benchmark-results-mobile.svg">
  <img src="/assets/grounding-benchmark-results.svg" alt="Pooled over 14 runs and 4,350 extractions. Wrong extractions accepted without review: LangExtract MATCH_EXACT 98.3 percent, groundgate 6.8 percent. Correct extractions citing the right place, rejected: MATCH_EXACT 4.6 percent, groundgate 0.3 percent. Extractions sent to a person: MATCH_EXACT none, groundgate 12.1 percent.">
</picture>
*groundgate let 8 of 117 wrong extractions through against 115 for MATCH_EXACT, and sent one in eight to a person. All 14 runs pooled. They share documents, so read the chart as an inventory of failures rather than a rate to expect; the per-run tables have intervals.*

Only 117 of the 4,350 extractions were wrong, so the price of catching them is review. groundgate sent 526 extractions to a person, one in eight, and 92 of them were wrong. A random sample of the same size would have held about 14.

Among correct extractions that cited the right place, groundgate rejected 14. Filtering on MATCH_EXACT dropped 194, every one because the quote aligned approximately rather than exactly. groundgate also rejected 71 correct values that LangExtract had aligned to a place that doesn't state them. The value was right and the evidence wasn't, so those rejections are the gate doing its job.

A separate track plants one error at a time into correct extractions, with no model involved. It tests mechanisms, so its percentages are not error rates. MATCH_EXACT accepts every value ten times too large with the right quote, every comma read as a decimal point (184,500 as 184.5) and every wrong unit, and groundgate accepts none of them. A planted "more than" in front of the value gets past MATCH_EXACT every time. groundgate sends 90% of those to review, and the 8.5% it admits cite a second place that states the same value without the planted words. On clean extractions it costs 9%: 7.6% go to review and 1.4% are rejected.

The one plant groundgate can't see is the one the real runs hit. Swap in another real number with the same unit from the same chunk, and groundgate admits 81%, because every check passes.

## Disagreement caught 84 of 109

I expected the value checks to carry the real runs. They caught 11. Hard rejections, from the type, unit and value-in-span checks together, accounted for 17 of the 109 wrong extractions groundgate stopped. Flags sent the other 92 to a person, and one flag did most of that work. `CONFLICTING_CANDIDATES`, raised when two proposals for a single-valued field disagree, was the first reason code on 84 of the 109.

In the conflicts I sampled, most pairs came from chunking. LangExtract sends a long document to the model a chunk at a time, and the model answers each chunk as if it were the whole document. The chunk with lisinopril's hypertension dosing says 10 mg. The chunk with renal impairment dosing says 5 mg. Both are real numbers, cited correctly, for the same field. groundgate can't tell which is right, so both go to a person, the right one included.

Chunk size moves both sides. LangExtract's default 1,000-character chunks produced 86 wrong extractions against 31 at 4,000, and conflicts were the first reason code on 69 of the 86. Bigger chunks cut the errors and also the disagreements that catch them: groundgate let 5 of 86 through at 1,000 characters and 3 of 31 at 4,000.

## The eight that got through

All eight are real numbers, cited correctly, with the right unit, and seven of them fill a field the document never states.

Five models answered metoprolol's maximum daily dose for hypertension with 200 mg, citing "up to 200 mg of metoprolol succinate". It passes every check: the span is real, 200 is in it, and mg sits next to it. It is the heart failure maximum, and the label states no maximum for hypertension. Two models gave levothyroxine's full replacement dose, 1.6 mcg/kg/day, as a flat 1.6 mcg starting dose. The unit rule found `mcg` right after the number and stopped looking. The eighth gave lisinopril's renal impairment dose as the usual starting dose.

Six of the eight took a value stated for another condition, and none of the v0.1 checks can see that. Pooling all seven models' proposals into one `admit` call caught one of the eight, GPT-5.6 Terra's lisinopril answer at 4,000 characters, because the other models had proposed 10 mg. Nobody disagreed with metoprolol's 200 mg. Five models gave it and the other two gave nothing.

Spec 0.2 takes this on. A field whose value depends on a condition, such as a dose per indication or a limit per filing year, will name the condition, and the gate will check that the condition's words sit in the cited text or the heading above it. The unit rule also needs to read a compound unit such as mcg/kg/day to its end. I left the spec frozen for this benchmark, because tuning rules on the test set would inflate the numbers. I also left in three weaknesses I found while building the scorer, and they cost false flags here. The fixes get measured on new documents, and the work is [tracked in the open](https://github.com/mohanraj00/groundgate/milestone/1).

## The benchmark found a bug in my gate

At 4,000 characters, LangExtract's chunker cut "Altimeter Setting: 29.97" after "29.", and three models answered 29 from that chunk. The spec already said a span never reads a prefix of a longer number. My code ran that check only when the span ended on a digit. This span ended on the decimal point, so the gate admitted 29.

I fixed the code, added the case to the evidence vectors, and report both numbers: 11 escapes before the fix, 8 after.

## What to do in any extraction pipeline

- Check the value at the citation. A quote match says nothing about the number you stored, and in the planted track MATCH_EXACT accepted every tenfold, comma and unit error.
- Keep every disagreement. Two answers to one field were the first reason code on 84 of the 109 wrong extractions stopped here, and a pipeline that keeps the last answer throws that signal away.
- Give the gate a third outcome. 92 of those 109 went to a person rather than a hard reject, at a cost of 12% of extractions reviewed.
- Let a field be absent, and name its condition. Seven of the eight escapes filled a field the document doesn't state.
- Don't count on a second model. When five models agreed on metoprolol's 200 mg, pooling had nothing to flag.
- Test the gate on real documents. My conformance cases missed a bug that one NTSB report found.

## Limits

Thirty documents and seven models show where the failure classes are. They are not enough to rank models. Claude drafted the gold, and three of the seven models are Claude models. I never saw the benchmarked models' output while checking, but drafts anchor judgment. The check kept nearly all of the draft: it excluded one field, found one absence the draft had wrong, and added two evidence places. The Claude runs did not make the fewest wrong extractions; Gemini 3.8 Flash did.

Every model ran through a logged-in agent CLI rather than a raw API, sandboxed and told not to use tools, so the results describe these setups rather than API-level model ability. The run script would discard and retry a Codex reply that used a tool, or a Claude Code reply with more than one turn or from a fallback model. None needed it. LangExtract skipped 69 of 2,240 chunks whose replies it couldn't parse. I couldn't set the temperature, so a rerun gives different extractions. I scored the cached runs.

The benchmark counts reviews. It doesn't measure how long a review takes or how often a reviewer gets it right. groundgate 0.1 also leaves out dates, lists of records and cross-document checks, and it never judges what a sentence means; the spec lists these as non-goals. The method, the caveats and every escape are in the [benchmark write-up](https://github.com/mohanraj00/groundgate/blob/main/bench/README.md) and the [results](https://github.com/mohanraj00/groundgate/blob/main/bench/RESULTS.md).

groundgate 0.1.0 is on [PyPI](https://pypi.org/project/groundgate/). Run `pip install groundgate`, and the README quickstart runs offline with no API key.

LangExtract locates the text. groundgate checks the number in it.
