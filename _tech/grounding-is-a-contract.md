---
title: "Grounding is a contract, not a citation"
date: 2026-09-29
image: /assets/heroes/grounding-is-a-contract.png
description: "LLMs get most extracted numbers right, and the wrong ones arrive with real citations. groundgate checks each value against its citation. Across 4,350 extractions it let 8 of 117 wrong values through; keeping only LangExtract's exact matches let 115."
---

I'm building a stealth vertical AI platform that extracts data from authoritative documents, and the numbers it extracts end up on money paths. If you've pulled numbers out of a PDF with Gemini, NotebookLM or LangExtract, you've probably found that the models are usually right. My benchmark agrees. Across seven models and 30 government documents, 4,233 of 4,350 extractions were correct.

This post is about the other 117. That is about 1 in 37, and nothing on the page tells you which ones. Every one of them cited a real place in its document, and keeping only exact matches still let 115 through. I built [groundgate](https://github.com/mohanraj00/groundgate) to catch them, and it let 8 through.

## A wrong number with a real citation

IRS Publication 560 has these two sentences, a few lines apart:

> The limit on elective deferrals, other than catch-up contributions, is <mark>$23,500</mark> for 2025 and $24,500 for 2026.
>
> The limit on salary reduction contributions, other than catch-up contributions, is <mark>$16,500</mark> for 2025 and increases to $17,000 for 2026.

The first is the 401(k) limit. The second is the SIMPLE plan limit, under its own heading.

I asked for the 2025 elective deferral limit. In 4 of the 14 runs, the model answered with both numbers. Each answer quoted its sentence word for word, and LangExtract marked both as <abbr title="LangExtract's strictest alignment status: the quoted text appears in the source character for character.">MATCH_EXACT</abbr>. Open either citation and it checks out: the sentence is real, and the number is in it.

The model didn't invent anything. LangExtract sends a long document to the model in chunks, and the model answers each chunk as if it were the whole document. The two sentences landed in different chunks, at both chunk sizes, so the model reading the SIMPLE chunk gave the closest match in that chunk. A reviewer who opens that citation sees $16,500 in a sentence about contribution limits. Catching it means knowing what a SIMPLE plan is, and reading that carefully on every fact.

The second example is simpler. Publication 15-B says supplemental wages over "$1 million" are withheld at 37%. GPT-5.6 Terra stored the threshold as 1, at both chunk sizes, and the quote "$1 million" matched exactly. A payroll rule that reads that field applies the 37% rate to anything over a dollar.

## What groundgate checks

LangExtract does what it promises: it finds where each quote sits in the source. The value you store is a separate attribute, and nothing compares it with the quote. LangExtract never claims to. A citation says where to look. The contract also says what that place must support: this value, in this unit, for this field, with nothing next to it that changes the meaning.

groundgate checks that contract between the model and your data. For every proposed fact, it checks that:

- the cited text contains the value as a number, and not as part of a longer number;
- the field's unit is next to it;
- no word next to it changes its meaning, such as "more than" before it or "million" after it;
- no other proposal gives the same field a different value.

Each fact gets one of three outcomes: admitted, sent to a person with the cited text to read, or rejected with a reason code. Both IRS examples go to a person. The deferral limit has two proposals that disagree, and "$1 million" has a scale word after the number. Every run writes a receipt that records each input's hash, and anyone can re-derive it with `groundgate verify`.

<picture>
  <source media="(max-width: 600px)" srcset="/assets/grounding-admission-gate-mobile.svg">
  <img src="/assets/grounding-admission-gate.svg" alt="A document goes to an extractor, an LLM running through LangExtract, which proposes candidate facts, each with a value, a unit and a cited span. A dashed admission boundary separates proposing from deciding. On the deciding side, groundgate runs value, unit, qualifier and conflict checks and sends each candidate to one of three outcomes: admitted into the dataset, needs verification and routed to a person with the span, or rejected with a reason code. Next to groundgate, a receipt records hashes of every input and can be re-derived by anyone.">
</picture>
*Every proposed fact leaves with one outcome and its reason codes. I use the same split for [coding agents](/tech/parallel-coding-agents-authority/): the component that produces a result never approves it.*

groundgate never calls a model, so the same inputs always give the same decisions. The whole benchmark went through it in 0.7 seconds, against about five hours of model time.

## Where it goes in your pipeline

It goes after your extractor and before anything writes to your database. It is for pipelines that store extracted values; a NotebookLM chat has no such step. You keep your extractor. groundgate needs the document text, a schema of your fields, and the proposed facts with their citations. With LangExtract, that is one call:

```python
import langextract as lx
from groundgate.adapters.langextract import admit_document

schema = {"fields": {
    "elective_deferral_limit_2025": {"type": "integer", "unit": "USD"},
    "supplemental_wage_threshold": {"type": "integer", "unit": "USD", "comparator": "gt"},  # "exceed"
}}

result = lx.extract(text_or_documents=text, prompt_description=prompt, examples=examples)
receipt = admit_document(result, schema)

for d in receipt.decisions:
    if d.outcome == "admitted":
        save(d.field, d.value)            # your database
    elif d.outcome == "needs_verification":
        review_queue.put(d)               # d.codes says why, d.evidence says where to read
    else:
        log_rejection(d)                  # rejected, with its reason codes
```

Without LangExtract, call `groundgate.admit(text, schema, candidates)` with proposals that give the position of their quote in the text. The [guide](https://github.com/mohanraj00/groundgate/blob/main/docs/guide.md) covers schemas and the candidate format, and the command line also turns PDFs into the text groundgate checks.

Three decisions come with it:

- **Who reviews.** One extraction in eight went to a person in my benchmark. That is the price of catching the wrong ones.
- **Keep every answer.** A pipeline that keeps the last answer for each field throws away the disagreement that caught most errors. Pass all of them to the gate.
- **Test a bigger chunk size.** On my documents, LangExtract's default 1,000-character chunks produced 86 wrong extractions, and 4,000-character chunks produced 31.

## What the benchmark found

<picture>
  <source media="(max-width: 600px)" srcset="/assets/grounding-benchmark-results-mobile.svg">
  <img src="/assets/grounding-benchmark-results.svg" alt="Pooled over 14 runs and 4,350 extractions. Wrong extractions accepted without review: LangExtract MATCH_EXACT 98.3 percent, groundgate 6.8 percent. Correct extractions citing the right place, rejected: MATCH_EXACT 4.6 percent, groundgate 0.3 percent. Extractions sent to a person: MATCH_EXACT none, groundgate 12.1 percent.">
</picture>
*All 14 runs pooled: 7 models, 2 chunk sizes, 30 documents. The runs share documents, so read this as an inventory of failures, not a rate to expect.*

Of the 117 wrong extractions, keeping only exact matches let 115 through. groundgate let 8 through. It rejected 17 outright and sent 526 extractions to a person, and those 526 held 92 of the wrong ones. A random sample of 526 would have held about 14.

Review is the cost: 434 of the 526 were correct, and a person had to confirm them. Outright rejection of a correct value was rare. Of the correct extractions that cited the right place, groundgate rejected 0.3%. Keeping only exact matches dropped 4.6%, because a quote that aligns approximately fails that filter even when its value is right.

Disagreement did most of the work. Two answers for one field was the first reason code on 84 of the 109 wrong extractions groundgate stopped. I expected the value-in-text check to carry the benchmark, and it was first on 11.

## What got through

All eight escapes cite a real sentence with the number in it, and all eight pass the unit check. Seven of them fill a field the document never states.

Five models gave metoprolol's maximum dose for hypertension as 200 mg, citing "up to 200 mg of metoprolol succinate". That is the heart failure maximum. The label states no maximum for hypertension. Each run gave that one answer, so there was no disagreement to flag, and no check on the cited text alone can see the problem. Two models gave levothyroxine's full replacement dose, 1.6 mcg/kg/day, as a flat 1.6 mcg starting dose. One gave lisinopril's renal impairment dose as the usual starting dose.

Spec 0.2 took this on. A field can now list its conditions, such as a drug's indications, and each proposed value names one. The gate checks that the condition is mentioned in the value's sentence or the nearest heading above it. A dose per kilogram also no longer passes as a flat dose.

Rules written from these escapes can't be measured on these documents, so I picked 101 new ones by rules frozen before anyone read them. They were chosen to stress these cases, so spec 0.1 does worse there than here. On the 74 documents checked in full, spec 0.1 let 30.7% of wrong extractions through and spec 0.2 let 8.8% through. The price is review: 39.6% of extractions went to a person, up from 28.2%. Every escape is listed in the [second set's results](https://github.com/mohanraj00/groundgate/blob/main/bench/set2/RESULTS.md).

<details class="inset" markdown="1">
<summary>How I measured it</summary>

I wrote the method before any model ran and scored against spec 0.1, frozen at one commit.

The documents are public domain: 10 FDA drug labels (dosage and strength sections), 10 NTSB aviation accident reports, and the first two pages of 10 IRS publications. Selection rules were fixed in advance, and the two documents I used while building groundgate are excluded. Each document has its own fields, such as doses, pilot hours, weather readings and contribution limits.

Claude drafted the gold answers. I checked all 277 facts and 33 absent fields by hand in 2.4 hours, in a labeling app that never shows the benchmarked models' output.

Each model ran through LangExtract at chunk sizes of 1,000 and 4,000 characters, for 14 runs. The models were Gemini 3.6 Flash and Gemini 3.8 Flash through the Antigravity CLI, GPT-5.6 Luna and GPT-5.6 Terra through Codex, and Claude Sonnet 5.5, Haiku 4.5 and Sonnet 4.6 through Claude Code. Every raw reply is cached, so CI rescores the benchmark byte for byte with no API key.

A second track plants one error at a time into correct extractions, with no model involved. Keeping only exact matches accepted every tenfold error, every comma read as a decimal point and every wrong unit. groundgate accepted none of them. Its blind spot is the one the real runs hit: swap in another real number with the same unit from the same chunk, and groundgate admits 81%.

</details>

<details class="inset" markdown="1">
<summary>The benchmark found a bug in my gate</summary>

At 4,000 characters, LangExtract's chunker cut "Altimeter Setting: 29.97" after "29.", and three models answered 29 from that chunk. The spec already said a value must never be read from part of a longer number. My code ran that check only when the cited text ended on a digit. This one ended on the decimal point, so the gate admitted 29.

I fixed the code, added the case to the conformance vectors, and report both numbers: 11 escapes before the fix, 8 after.

</details>

<details class="inset" markdown="1">
<summary>Limits</summary>

Thirty documents and seven models show where the failure classes are. They are not enough to rank models. Claude drafted the gold, and three of the seven models are Claude models. I never saw model output while checking, but a draft anchors judgment. The Claude runs did not make the fewest wrong extractions; Gemini 3.8 Flash did.

Every model ran through a logged-in agent CLI, not a raw API, so the results describe these setups. I couldn't set the temperature, so a rerun gives different extractions; I scored the cached runs. LangExtract skipped 69 of 2,240 chunks whose replies it couldn't parse.

The benchmark counts reviews. It doesn't measure how long a review takes or how often a reviewer gets it right. groundgate leaves out dates, lists of records and cross-document checks, and it never judges what a sentence means.

</details>

The method, every escape and the per-run tables are in the [benchmark write-up](https://github.com/mohanraj00/groundgate/blob/main/bench/README.md) and the [results](https://github.com/mohanraj00/groundgate/blob/main/bench/RESULTS.md). groundgate is an Apache-2.0 Python library with no core dependencies, on [PyPI](https://pypi.org/project/groundgate/). The current release is 0.3.0, and the numbers in this post are spec 0.1's. Run `pip install groundgate`; the README quickstart runs offline with no API key.

LangExtract locates the text. groundgate checks the number in it.
