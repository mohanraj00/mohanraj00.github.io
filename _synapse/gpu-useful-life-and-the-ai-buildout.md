---
title: "The AI boom runs on a guess about how long a server lasts"
date: 2026-08-05
synapse: 7
tags: [accounting, artificial-intelligence, finance, capital-expenditure]
excerpt: "Depreciation turns AI spending into reported profit through a number that accounting rules openly call an estimate. On the same day in January 2025, citing the same cause, Amazon shortened it and Meta lengthened it."
image: /assets/heroes/gpu-useful-life-and-the-ai-buildout.png
hero_hue: 32
---

I went looking for something dull and found an argument.

The dull thing was depreciation. My accounting notes describe useful life as an estimate that management sets when an asset goes into service, and then say, almost apologetically, that it is common for the estimate to turn out wrong. It is the sort of sentence you read past.

Then I checked what the four companies spending the most money in the world on AI hardware actually put in their filings. They do not agree. Effective 1 January 2025, Amazon shortened the assumed life of some of its servers from six years to five. Effective that same day, Meta lengthened most of its own to five and a half. Both pointed at the pace of AI as the reason.

Not analysts arguing with companies. The companies disagreeing with each other, in public, about the same asset class, taking effect on the same date.

<div class="synapse-watch" style="max-width:320px;margin:2rem auto;">
  <div style="position:relative;padding-bottom:177.78%;height:0;overflow:hidden;border-radius:12px;">
    <iframe src="https://www.youtube-nocookie.com/embed/nkf1UkoFxYo" title="The AI boom runs on a guess about how long a server lasts — a Midweek Synapse Short" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"></iframe>
  </div>
  <p style="text-align:center;margin:.6rem 0 0;font-size:.9rem;"><em>The 53-second version. Watch on <a href="https://youtube.com/shorts/nkf1UkoFxYo">YouTube</a> or <a href="https://www.instagram.com/p/DbxPv5ushud/">Instagram</a>.</em></p>
</div>

## Why a number nobody talks about moves billions

Depreciation spreads what you paid for something across the years you expect it to earn. Buy a server for six hundred thousand dollars, assume six years, and you book a hundred thousand a year as expense. Assume four years, and you book a hundred and fifty thousand. Same server, same cash out the door, different profit on the page.

Stretch the assumed life and this year's expense shrinks, so this year's reported profit grows. Do it across a fleet the size of a hyperscaler's and the effect is enormous, and it lasts for years.

The companies disclose exactly how enormous, which is the part I did not expect. Microsoft moved server and network equipment from four years to six for fiscal 2023, and its own filing puts the effect at an extra $3.7 billion of operating income and $3.0 billion of net income, forty cents a share. Alphabet made a matching change in January 2023: depreciation expense down $3.9 billion, net income up $3.0 billion, twenty-four cents a share.

Those are not rounding errors dressed up as disclosure. Each one is larger than the entire annual profit of most public companies, and each came from revising a single estimate.

## The fork

<img src="/assets/synapse/gpu-useful-life-divergence.svg" alt="A step chart from 2022 to 2026 showing the assumed useful life of a server at four companies. Microsoft steps from four years to six from fiscal 2023. Alphabet steps from four to six in January 2023. Amazon steps from five to six in January 2024, then back down to five in January 2025 for a subset of servers. Meta holds at five years and steps up to five and a half in January 2025. The two January 2025 changes take effect on the same day and move in opposite directions: Amazon's cut its 2025 net income by one billion dollars, Meta's raised its 2025 net income by two point five nine billion." style="max-width:100%;height:auto;">

*Four firms, one asset class, and a day where two of them go opposite ways.*

Amazon's filing gives the reason for shortening in plain words: "the increased pace of technology development, particularly in the area of artificial intelligence and machine learning." The change cost it $1.0 billion of 2025 net income, mostly at AWS.

Microsoft, two and a half years earlier, had cited "advances in technology" as part of its reason for going the other way.

The same force, technological progress, is offered by one company as grounds for a shorter life and by another as grounds for a longer one. Both statements are audited. Neither is wrong in any way a regulator would care about. That is what an estimate looks like when it is doing real work.

There is a detail here that most of the commentary I read skips, and it is the one I find hardest to explain away. Amazon did not simply take a more conservative view than its peers. It reversed itself. It had extended servers from five years to six effective 1 January 2024, then pulled a subset back to five effective 1 January 2025. Thirteen months, two directions.

## The best argument that everyone is fine

The strongest case against reading any of this as flattered earnings comes from Nvidia, and it is worth taking seriously.

On 19 November 2025, CFO Colette Kress used her prepared remarks, not an answer squeezed out of her in Q&A, to make an explicitly accounting-shaped claim: CUDA's compatibility and Nvidia's installed base "extend the life NVIDIA systems well-beyond their original estimated useful life." And then the line that got quoted everywhere: "thanks to CUDA, the A100 GPUs we shipped six years ago are still running at full utilization today, powered by vastly improved software stack."

If that is broadly true, the longer estimates are not generous, they are accurate. The mechanism is a cascade: the newest silicon takes frontier training, last generation's moves to fine-tuning, older cards end up serving routine inference, and a GPU keeps earning long after it stops being the fastest thing in the building.

Two honest qualifications. Nvidia is not a neutral party, because customers who believe their hardware lasts longer buy more of it. And the A100 entered full production on 14 May 2020, which made those chips about five and a half years old when she said six.

## The check that turns out not to exist

Here is where I expected to find a clean answer and did not.

Accounting has a backstop for exactly this worry. If an asset's book value drifts above what it is really worth, the rules require an impairment write-down. So if AI hardware were quietly dying at two or three years while being depreciated over six, impairments should be piling up. That is checkable, and it settles the question without needing anyone's opinion.

At Meta it checks out well for the companies. Property and equipment impairment losses were $738 million in 2023, $288 million in 2024, and $237 million in 2025. Falling, while depreciation on servers and network assets over the same three years went $7.32 billion, $11.34 billion, $13.36 billion. Impairments shrinking against a depreciation charge that nearly doubled is a real point in the companies' favour.

Then I went to run the same check on the other three, and could not.

Amazon's most recent filing names impairment of property and equipment as a critical estimate and explains the policy for recognising one, without giving an annual figure. Alphabet's and Microsoft's most recent filings quantify impairments for investments and for goodwill, but not for property and equipment. As far as I can find, Meta is the only one of the four that publishes the number at all.

So the strongest available evidence that the hardware is holding its value rests on one company's voluntary disclosure. Not because the other three look worse. Because there is nothing there to look at. The backstop everyone points to is, for three quarters of the group, invisible from outside.

## What I am not claiming

There is a widely reported figure floating around this debate, from investor Michael Burry, putting the industry's overstatement at roughly $176 billion across 2026 to 2028. I could not trace it to anything he published directly, only to coverage of his posts, so I have deliberately kept it out of the argument. Everything above stands on filings alone.

I also cannot tell you who is right. That is not a hedge, it is the finding. Utilization data for hyperscaler fleets is not disclosed, so the economic life of an AI accelerator is not knowable from the outside. What the filings do establish beyond argument is that the disagreement is real, it is between the companies rather than about them, and it is worth billions a year in reported profit.

One thing I keep turning over. My notes say units of production depreciation, where you expense an asset by how much you actually use it rather than by how long you have owned it, is the right method when an asset is consumed by use rather than by time. A GPU's life is surely measured in tokens served more than in calendar years. Not one of these firms depreciates that way. I do not know whether that is a measurement problem, a disclosure convenience, or a quiet signal that nobody really believes GPU life is usage bound.

What I take from the week is smaller and more useful than a verdict. The largest capital cycle in corporate history passes through an estimate, the estimate is disclosed, and reading the disclosure is free. [Last time](/synapse/three-theories-of-disruption/) it was a word doing more work than anyone noticed. This time it is a number.

## Sources

Every figure above is from the company's own filing on SEC EDGAR rather than from commentary. Direct links, in case you want to read the sentence yourself:

- [Microsoft Form 10-K, FY2023](https://www.sec.gov/Archives/edgar/data/789019/000095017023035122/msft-20230630.htm), for the four-to-six-year change and its $3.7 billion effect.
- [Alphabet Form 10-K, FY2023](https://www.sec.gov/Archives/edgar/data/1652044/000165204424000022/goog-20231231.htm), for the January 2023 assessment and the $3.9 billion depreciation reduction.
- [Amazon Form 10-K, FY2025](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm), for the shortening effective 1 January 2025, the AI reason quoted verbatim, and the 2024 extension it reversed.
- [Meta Form 10-K, FY2025](https://www.sec.gov/Archives/edgar/data/1326801/000162828026003942/meta-20251231.htm), for the 5.5-year extension, the $2.59 billion net income effect, and the impairment figures.
- [Nvidia Q3 FY2026 earnings call transcript, 19 November 2025](https://s201.q4cdn.com/141608511/files/doc_financials/2026/q3/NVDA-Q3-2026-Earnings-Call-19-November-2025-5_00-PM-ET.pdf), Nvidia's own copy, for Colette Kress's remarks on CUDA and useful life.
- [Nvidia's A100 full production announcement, 14 May 2020](https://nvidianews.nvidia.com/news/nvidias-new-ampere-data-center-gpu-in-full-production), for dating the "six years ago" claim.

Part of #MidweekSynapse, my weekly quest to learn in public.
