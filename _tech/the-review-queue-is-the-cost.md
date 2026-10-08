---
title: "The review queue is the cost"
date: 2026-10-08
image: /assets/heroes/the-review-queue-is-the-cost.png
description: "A gate can stop almost every wrong value by sending everything to a person. groundgate now scores each rule by right values admitted and wrong values admitted, and lets a recorded model answer clear one kind of flag without letting the model decide."
---

In [the first post](/tech/grounding-is-a-contract/), groundgate admitted 8 of 117 wrong extractions, where LangExtract's exact matches admitted 115. The price was review. groundgate sent one extraction in eight to a person.

Then I picked 101 new documents with the cases that escaped: doses that change by indication, doses per kilogram, amounts such as "$1.2 million". On the 74 that I checked in full, the spec 0.2 rules cut the share of wrong extractions admitted from 30.7% to 8.8%. They also sent 39.6% of all extractions to a person, up from 28.2%.

A gate that sends four facts in ten to a person is too slow to run.

So I changed what I measure. Every rule now gets two numbers: the right values it admits, and the wrong values it admits. Reviews are the cost between them, because each review is a value that a person confirms by hand. A rule that cuts escapes by adding reviews is not free. The best rule admits more right values with no new escape.

This post covers two changes that target that cost. In the first, the extractor cites every part of a value. In the second, a model's answer becomes a recorded input to the gate. That answer can clear one flag, and the gate still makes every decision.

## Most reviews are right values

A rule that is unsure sends the value to a person, and most of those values are right. Spec 0.3 reads a flattened dose table by its lines. On 62 doses in such tables, the wrong indication went from 60 doses to none, and the right indication went from 55 doses to 3. So 52 right doses now go to review with the wrong ones.

## Let the extractor cite every part

A 10-K table states "(in thousands)" once, at the top. A row states "18,789". Claude Haiku 4.5 scales table numbers, so it returned 18789000, which is right. Spec 0.3 rejected it, because no single quote in the document holds 18789000.

The value was right. Its evidence was in two places, and groundgate could check only one.

Spec 0.5 lets the extractor cite each part of a value where it is: the number, its sign, its scale, its unit, the row label and the column heading. groundgate checks each part and computes the value from them. Here is one candidate, from a made-up statement table in the guide:

```json
{"field": "operating_income", "key": "2025", "value": "-3415000", "unit": "USD",
 "evidence": [{"role": "value", "text": "(3,415)"},
              {"role": "scale", "text": "(in thousands)"},
              {"role": "unit",  "text": "$"},
              {"role": "field", "text": "Loss from operations"},
              {"role": "key",   "text": "2025"}]}
```

The brackets make the value negative. The scale multiplies it by a thousand. When a part that the value needs has no citation, the value goes to review with that part named. It is not rejected.

On 20 new 10-K filings, spec 0.4 admitted 23 right values and 1 wrong one. Spec 0.5 admitted 26 right values and no wrong one, and sent 13 values to review for a missing part. On an IRS filing-status set, both specs admitted the same 28 right values, and spec 0.5 sent 20 values to review for a missing part. The change gave no gain there. One rule costs right values on the 10-K set: a unit item fails when the unit is already next to the number. Without that rule, spec 0.5 admits 33. The fix is open for 0.6.

## A model answer as a recorded input

Some flags are mostly false alarms. In the test part of a second 10-K set, 40 filings, 53 values had the flag `KEY_NOT_AT_VALUE`: groundgate could not find the fiscal year at the value. At 51 of them, the value had the right year. A column heading a few lines up is easy for a person and hard for a text rule.

A small model reads that context well. groundgate exists because the component that produces a fact must never approve it. A gate that calls a model also cannot promise the same decision twice.

Spec 0.4 keeps both properties, because the model's answer is a recorded input, not a call:

1. Before the decision, a judge model answers one question about one flagged value, such as "which fiscal year is this value for?". You store the answer and its probability.
2. The policy names one judge, one model version, and one threshold for each question.
3. groundgate reads the stored answer. If the judge picks the candidate's own key at or above the threshold, the flag clears with `MODEL_CLEARED`. If it picks another key or none, the value gets `MODEL_DOUBT`.
4. The receipt lists every judgment that applied. `groundgate verify` takes the same judgments and re-derives the receipt byte for byte.

```python
policy = {"judge": {"id": "my-judge", "digest": "my-judge-1.0",
                    "clear": {"KEY_NOT_AT_VALUE": 0.5}}}
receipt = gg.admit(text, schema, candidates, policy, judgments=judgments)
```

The spec sets two limits. A judgment never overturns a rejection. A judgment never admits a value that has another flag. If the cleared flag was the only one, every check on the value has passed, and the gate admits it.

On that test part, the judge at 0.5 cleared 34 of the 51 right flags, with no escape. The FDA labels gave the same threshold. The test part held only 2 wrong flags, so the escape result uses few data. The second question asks whether a value is the field at all. With the FDA threshold, it caught 0 of 6 wrong values and sent 5 right ones to review.

A threshold belongs to one model and one kind of document, so groundgate ships none. `groundgate-calibrate` measures yours on your own documents. It is not on PyPI yet.

## Where it goes in a pipeline now

You do not need LangExtract. `gg.extractor_schema(schema)` builds a JSON Schema for your model's structured output, in the subset that strict output modes accept. Your schema fixes the field, unit and keys that the model can return.

1. Your model proposes candidates with their quotes.
2. Optionally, a judge answers questions about flagged values, and you store the answers.
3. groundgate decides each candidate from the document, the schema, the policy and the stored answers.
4. Admitted values go to your database. Values for review go to a person, with the reason and the place to read. A [how-to](https://github.com/mohanraj00/groundgate/blob/main/docs/howto/feedback.md) sends the reasons back to the model once, for a second try.

<details class="inset" markdown="1">
<summary>How I measure a rule</summary>

Every rule comes from a failure, so I never measure it on the documents it came from. Each rule gets a new set of documents, picked by rules that I froze before anyone read them. A person labels the set blind, before scoring. The changelog names the measure and the set for each release, and CI rescores the sets from cached model output.

The numbers in this post come from small sets: 62 table doses, 20 new 10-K filings with one extractor run, and a judge test part with 2 wrong flags. They show which way a rule moves the two numbers. They are not rates to expect on your documents.

</details>

<details class="inset" markdown="1">
<summary>What is open</summary>

- In a table "(in thousands)", a value given unscaled with no scale item is admitted ([#162](https://github.com/mohanraj00/groundgate/issues/162)). That is a path for an escape, and it is planned for 0.6.
- The unit rule above costs right values on the 10-K set.
- The one built-in judge is a hosted model. It sends a window of each document out of the machine.
- groundgate reads English number formats only, and it does not read dates or lists of records.

</details>

groundgate 0.5.1 is on [PyPI](https://pypi.org/project/groundgate/) under Apache-2.0. The [changelog](https://github.com/mohanraj00/groundgate/blob/main/CHANGELOG.md) has every rule with its measure.

The model proposes, and it can confirm one thing. Only the gate admits.
