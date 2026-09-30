---
title: "Grounding is a contract, not a citation"
date: 2026-09-29
image: /assets/heroes/grounding-is-a-contract.png
---

I'm building a stealth vertical AI platform. Much of what it knows comes from documents, and the numbers it extracts land on money paths. A wrong number on a money path rarely looks wrong. It arrives with a confident value and a citation to a real sentence.

Every fact in my pipeline already goes through value checks I wrote myself. [LangExtract](https://github.com/google/langextract) promises to map "every extraction to its exact location in the source text", and before building on it I needed to know whether that grounding made my checks redundant. The question was narrow: when a model extracts the wrong value, does grounding catch it?

So I measured it. Seven models ran through LangExtract on 30 public-domain government documents, with a person-checked answer for every fact the benchmark asks for. They produced 117 wrong extractions. LangExtract's strictest setting accepted 115 of them.

## What grounding checks

LangExtract does what it promises. It finds where each extraction's quoted text sits in the source and reports how well the quote aligned. It never compares the value you asked for with that text. This is an extraction LangExtract reports as an exact match:

```text
extraction_text: "$8,000"     found in the source: MATCH_EXACT
value:           "80000"      not what the source says
```

The quote is real. The number attached to it is off by ten, and nothing downstream has a reason to doubt it, because it has a citation.

## Extraction and admission are different problems

An extraction pipeline answers one question: what does this document say? A pipeline whose output becomes a dataset or a decision has a second one. Should this fact be admitted at all?

I keep the two apart for the same reason I keep [building and verifying apart for coding agents](/tech/parallel-coding-agents-authority/). The thing that produces the work never gets to approve it. The model proposes. A deterministic gate decides, and every fact leaves one of three ways.

![Left to right. A document goes to an extractor, which proposes candidate facts, each citing a span of the document. The candidates cross an admission boundary into groundgate, which runs deterministic checks. Each candidate leaves with one of three outcomes: admitted into the dataset, needs verification and routed to a person with the evidence location, or rejected with a reason code. Every run also writes a receipt that anyone can re-derive from the inputs.](/assets/grounding-admission-gate.svg)
*The model proposes; the gate decides, and writes down why.*

I built that gate as [groundgate](https://github.com/mohanraj00/groundgate), an Apache-2.0 Python library with no dependencies in its core. It takes the document, a schema of the fields you want, and the candidates an extractor proposed. For each candidate it checks that the value is a number written inside the cited span and that the field's unit sits at that number. It flags a qualifier that changes the meaning, such as "more than" before a field that means "at least", and a scale word such as "million" after the number. It also flags two proposals for one field that disagree. A fact that fails a check is rejected with a stable reason code. A fact that passes with a warning goes to a person, with the place to look.

It never calls a model, so the same inputs give the same decisions every time. Evidence is a UTF-8 byte span, and a span never reads a prefix of a longer number. The rules live in a written [spec](https://github.com/mohanraj00/groundgate/blob/main/SPEC.md) with 16 language-neutral conformance vectors, so an implementation in another language can prove it agrees. Every run writes a receipt hashed over RFC 8785 canonical JSON, and `groundgate verify` re-derives it byte for byte, so anyone can audit a decision without trusting the run that made it.

LangExtract stays in the pipeline. It is published under Google's GitHub organisation, and its README says it is not an officially supported Google product. Its alignment is the reason the evidence spans exist at all. groundgate reads LangExtract's output directly and checks each extraction's value and unit at the place LangExtract aligned it.

## How I measured it

A claim like "LangExtract lets wrong values through" is only as good as its method, so I fixed the method before any model ran.

The documents are public domain and were picked by fixed rules: 10 FDA drug labels (dosage and strength sections), 10 NTSB aviation accident reports, and the first two pages of 10 IRS publications. Each document gets its own fields, such as starting and maximum doses, pilot hours and weather readings, contribution limits and phase-out thresholds.

Claude drafted the gold. I checked all of it in a small labeling app that never shows what the benchmarked models extracted: 277 facts and 33 fields the documents do not state, in 2.4 hours. Tables were the slow part. PDF text flattens an IRS table into a list of row labels followed by a list of values, so the app links to the original page.

Seven models proposed through LangExtract at two chunk sizes. Gemini 3.6 Flash and Gemini 3.8 Flash ran through the Antigravity CLI, GPT-5.6 Luna and GPT-5.6 Terra through Codex, and Claude Sonnet 5.5, Haiku 4.5 and Sonnet 4.6 through Claude Code. Every raw reply is cached, so CI rebuilds every score with no API key. I froze the spec before scoring.

![Pooled over 14 runs and 4,350 extractions. Wrong extractions accepted without review: LangExtract MATCH_EXACT 98.3 percent, groundgate 6.8 percent. Correct extractions rejected: MATCH_EXACT 4.6 percent, groundgate 0.3 percent. Extractions sent to a person: MATCH_EXACT none, groundgate 12.1 percent.](/assets/grounding-benchmark-results.svg)
*All 14 runs pooled. The runs share documents, so the chart carries no intervals; the per-run tables have them.*

groundgate admitted 8 of the 117 wrong extractions without review. It rejected 14 of 4,233 correct ones. MATCH_EXACT rejected 194 correct extractions, every one citing the right place, because the quote aligned approximately rather than exactly. The price is review: one extraction in eight goes to a person.

A separate track plants one error at a time into correct extractions, with no model involved. MATCH_EXACT accepts every value ten times too large with the right quote, every comma read as a decimal point (184,500 as 184.5) and every wrong unit. groundgate accepts none of them. Writing "more than" into the document in front of the value gets through MATCH_EXACT every time. groundgate sends 90% of those to review, and every one it admitted cited another place where the same text appears without the planted words.

## Disagreement caught the most

I expected the value checks to carry the real runs. They caught fewer than I thought. In these runs the models rarely misread a number they were looking at, and `VALUE_NOT_IN_EVIDENCE` stopped only 11. One flag caught 84 of the 109 wrong extractions groundgate stopped: `CONFLICTING_CANDIDATES`, two proposals for a single-valued field with different values.

Most of those pairs come from chunking. LangExtract sends a long document to the model a chunk at a time, and the model answers each chunk as if it were the whole document. The chunk with lisinopril's hypertension dosing says 10 mg. The chunk with renal impairment dosing says 5 mg. Both are real numbers, cited correctly, for the same field. groundgate cannot tell which one is right, so it sends both to a person. Smaller chunks produced nearly three times as many wrong extractions (86 against 31), and this flag stopped 69 of the 86.

## What got through

The eight escapes matter more than the average, because they show where a text-level gate ends.

Five models answered metoprolol's maximum daily dose with 200 mg, citing "up to 200 mg of metoprolol succinate". The sentence is real, the number is in it, and the unit is next to it. It is the heart failure maximum. The field asks for hypertension, which has no stated maximum. One model gave lisinopril's renal impairment dose as the usual starting dose. Two read levothyroxine's "1.6 mcg/kg/day" as a flat 1.6 mcg, because the unit rule finds `mcg` right after the number and stops looking.

Six of the eight are one failure: a real value, cited correctly, that belongs to another condition. The citation is real and the claim is wrong, and no span check can see the difference. Putting all seven models through one gate caught only one of them, GPT-5.6 Terra's lisinopril answer, because the other models had proposed 10 mg. Nobody disagreed with metoprolol's 200 mg. Five models gave it and the other two gave nothing. In this benchmark, when models were wrong, they were wrong together.

The fix belongs in spec 0.2. A field whose value depends on a condition, such as a dose per indication or a limit per filing year, should name the condition, and the gate should check that the condition's words sit in the cited text or the heading above it. I left the spec frozen for this benchmark, because tuning rules on the test set would make the numbers worthless. The fix gets measured on new documents, and the work is [tracked in the open](https://github.com/mohanraj00/groundgate/milestone/1).

## The benchmark found a bug in my gate

At the larger chunk size, LangExtract's chunker cut "Altimeter Setting: 29.97" after "29.", and three models answered 29 from that chunk. My spec already said a span never reads a prefix of a longer number. My code enforced that only when the span ended on a digit, so it admitted 29.

I fixed the code, added a conformance vector, and reported both numbers: 11 escapes before the fix, 8 after. A gate you trust with your data deserves the same test as the models it checks, on real documents, with every escape written down.

## What I'd do in any extraction pipeline

- Check the value at the citation. A quote match proves the text exists and says nothing about the number you stored.
- Keep every disagreement. Two chunks that answer one field differently were the strongest signal in these runs, and a pipeline that keeps the last answer throws it away.
- Give the gate a third outcome. Flags that send a fact to a person did most of the catching here, at a cost of 12% of extractions reviewed.
- Don't count on a second model to catch the first. Here, the models that were wrong agreed with each other.
- Test the gate the way you test the models. Mine had a bug that only real documents found.

## Limits

Thirty documents and seven models show where the failure classes are. They are not enough to rank models. Claude drafted the gold, and three of the seven models are Claude models. The person checking it never saw the benchmarked models' output, but drafts anchor judgment, and the check changed very little. Every model ran through a logged-in agent CLI rather than a raw API, sandboxed and told not to use tools. A Codex reply that used a tool was discarded and retried, and so was a Claude Code reply that took more than one turn or came from a fallback model. I could not set the temperature, so a rerun gives different extractions; the cached runs are what was scored. The method, the caveats and every escape are in the [benchmark write-up](https://github.com/mohanraj00/groundgate/blob/main/bench/README.md) and the [results](https://github.com/mohanraj00/groundgate/blob/main/bench/RESULTS.md).

groundgate 0.1.0 is on [PyPI](https://pypi.org/project/groundgate/). `pip install groundgate` and the README quickstart runs offline, with no API key.

LangExtract verifies the text. groundgate verifies the value.
