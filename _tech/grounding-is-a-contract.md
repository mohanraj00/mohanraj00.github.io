---
title: "Grounding is a contract, not a citation"
date: 2026-09-29
image: /assets/heroes/grounding-is-a-contract.png
---

I ran seven models through LangExtract on 30 public-domain government documents, with a person-checked answer for every fact the benchmark asks for. The models produced 117 wrong extractions. LangExtract's strictest setting accepted 115 of them.

LangExtract did what it promises. It finds where each extraction's quoted text sits in the source, and it never checks the value you asked for. This is an extraction LangExtract reports as an exact match:

```text
extraction_text: "$8,000"     found in the source: MATCH_EXACT
value:           "80000"      not what the source says
```

The quote is real. The number attached to it is off by ten. For anyone building a dataset out of LLM output, that gap is where wrong facts get in.

## Extraction and admission are different problems

An extraction pipeline answers one question: what does this document say? A pipeline whose output becomes somebody's dataset carries a second one: should this fact be admitted at all?

I keep the two apart. The model proposes. A deterministic gate decides, and every fact comes out one of three ways.

![Left to right. A document goes to an extractor, which proposes candidate facts, each citing a span of the document. The candidates cross an admission boundary into groundgate, which runs deterministic checks. Each candidate leaves with one of three outcomes: admitted into the dataset, needs verification and routed to a person with the evidence location, or rejected with a reason code. Every run also writes a receipt that anyone can re-derive from the inputs.](/assets/grounding-admission-gate.svg)
*The model proposes; the gate decides, and writes down why.*

I built the gate as [groundgate](https://github.com/mohanraj00/groundgate), an Apache-2.0 Python library with no dependencies in its core. It takes the document, a schema of the fields you want, and the candidates an extractor proposed. For each candidate it checks that the value is a number actually written inside the cited span, with the field's unit at that number, and that nothing next to it changes what it means: "more than" in front of a field that means "at least", "million" after it, or another proposal for the same field with a different value. A fact that fails a check is rejected with a stable code. A fact that passes but carries a warning goes to a person. The rules are written as a [spec](https://github.com/mohanraj00/groundgate/blob/main/SPEC.md) with language-neutral test vectors, and every run writes a hashed receipt that `groundgate verify` re-derives byte for byte.

[LangExtract](https://github.com/google/langextract) stays in the pipeline. It is published under Google's GitHub organisation (its README notes it is not an officially supported Google product), and its alignment is the reason the evidence spans exist at all. groundgate reads its output directly and checks each extraction's value and unit at the place LangExtract aligned it.

## The benchmark

A claim like "LangExtract lets wrong values through" needs a number, so I built one before calling the library done.

The documents are public domain and picked by fixed rules before any model ran: 10 FDA drug labels (dosage and strength sections), 10 NTSB aviation accident reports, and the first two pages of 10 IRS publications. Each document gets its own fields: starting and maximum doses, pilot hours and weather readings, contribution limits and phase-out thresholds.

Claude drafted the gold. I checked all of it in a small labeling app that never shows what the benchmarked models extracted: 277 facts and 33 fields the documents do not state, in 2.4 hours. Tables were the slow part. PDF text flattens an IRS table into a list of row labels followed by a list of values, so the app links to the original page.

Seven models proposed through LangExtract at two chunk sizes: Gemini 3.6 Flash and Gemini 3.8 Flash through the Antigravity CLI, GPT-5.6 Luna and GPT-5.6 Terra through Codex, and Claude Sonnet 5.5, Haiku 4.5 and Sonnet 4.6 through Claude Code. Every raw reply is cached, so the scores rebuild in CI with no API key.

![Pooled over 14 runs and 4,350 extractions. Wrong extractions accepted without review: LangExtract MATCH_EXACT 98.3 percent, groundgate 6.8 percent. Correct extractions rejected: MATCH_EXACT 4.6 percent, groundgate 0.3 percent. Extractions sent to a person: MATCH_EXACT none, groundgate 12.1 percent.](/assets/grounding-benchmark-results.svg)
*Every run pooled. The runs share documents, so the chart carries no intervals; the per-run tables have them.*

groundgate admitted 8 of the 117 wrong extractions without review. It rejected 14 of 4,233 correct extractions. MATCH_EXACT rejected 194, all of them correct values citing the right place, dropped because the quote aligned approximately rather than exactly. The price is review: one extraction in eight goes to a person.

A separate track plants one error at a time into correct extractions, with no model involved. A value ten times too large with the right quote, a comma read as a decimal point (184,500 as 184.5), the wrong unit: MATCH_EXACT accepts all of them and groundgate none. Writing "more than" into the document in front of the value gets through MATCH_EXACT every time; groundgate sends 90% of those to review, and every one it admitted cited another place where the same sentence appears without the planted words.

## Disagreement is the cheapest signal

I expected the value checks to carry the real runs. They caught fewer than I thought: in these runs the models rarely misread a number they were looking at, and `VALUE_NOT_IN_EVIDENCE` stopped only 11. 84 of the 109 wrong extractions groundgate stopped were caught by one flag, `CONFLICTING_CANDIDATES`: two proposals for a single-valued field with different values.

Most of those pairs come from chunking. LangExtract sends a long document to the model a chunk at a time, and the model answers each chunk as if it were the whole document. The chunk with lisinopril's hypertension dosing says 10 mg. The chunk with renal impairment dosing says 5 mg. Both are real numbers, cited correctly, for the same field. groundgate cannot tell which one is right, so it sends both to a person. Smaller chunks produced nearly three times as many wrong extractions (86 against 31), and this flag stopped 69 of the 86.

## What got through

The eight escapes matter more than the average, because they show where a text-level gate ends.

Five models answered metoprolol's maximum daily dose with 200 mg, citing "up to 200 mg of metoprolol succinate". The sentence is real, the number is in it, and the unit is next to it. It is the heart failure maximum; the field asks for hypertension, which has no stated maximum. One model gave lisinopril's renal impairment dose as the usual starting dose. Two read levothyroxine's "1.6 mcg/kg/day" as a flat 1.6 mcg, because the unit rule finds `mcg` right after the number and does not look further.

Six of the eight are one failure: a real value, cited correctly, that belongs to another condition. A citation can be real while the claim attached to it is wrong, and no span check sees it. Putting all seven models through one gate caught only one of them, GPT-5.6 Terra's lisinopril answer, because the other models had also proposed 10 mg. Nobody disagreed with metoprolol's 200 mg: five models gave it and the other two gave nothing. In this benchmark, when models were wrong, they were wrong together.

That is the next version's work. A field whose value depends on a condition (a dose per indication, a limit per filing year) should name the condition, and the gate should check that the condition's words sit in the cited text or the heading above it. I left the spec frozen for this benchmark, because tuning rules on the test set would make the numbers worthless. The fix gets measured on new documents.

## The benchmark found a bug in the gate

At the larger chunk size, LangExtract's chunker cut "Altimeter Setting: 29.97" after "29.", and three models answered 29 from that chunk. My spec already says a span never reads a prefix of a longer number. My code only enforced that when the span ended on a digit, so it admitted 29.

I fixed the code, added a conformance vector, and report both numbers: 11 escapes before the fix, 8 after. A gate you trust with your data should be tested the same way as the models it checks, on real documents, with every miss written down.

## Limits

Thirty documents and seven models show where the failure classes are. They are not enough to rank models. Claude drafted the gold, and three of the seven models are Claude models; the person checking it never saw model output, but drafts anchor judgment, and the check changed very little. Every model ran through a logged-in agent CLI rather than a raw API, sandboxed and told not to use tools. A Codex reply that used a tool was discarded and retried, and so was a Claude Code reply that took more than one turn or came from a fallback model. Temperature was not mine to set, so a rerun gives different extractions; the cached runs are what was scored. The method, the caveats and every escape are in the [benchmark write-up](https://github.com/mohanraj00/groundgate/blob/main/bench/README.md) and the [results](https://github.com/mohanraj00/groundgate/blob/main/bench/RESULTS.md).

groundgate 0.1.0 is on [PyPI](https://pypi.org/project/groundgate/). `pip install groundgate`, and the quickstart runs in a minute with no key.

LangExtract verifies the text. groundgate verifies the value.
