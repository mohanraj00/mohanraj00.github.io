---
title: "Only two people have won both a Turing Award and a Nobel Prize"
date: 2026-07-12
synapse: 3
tags: [artificial-intelligence, history-of-ai, bounded-rationality, deep-learning]
excerpt: "Both are AI researchers, on opposite sides of the field's oldest argument. The neat story is that each proved the other wrong. The truth is better."
---

The Turing Award is the top prize in computer science. The Nobel needs no introduction. Only two people have ever won both, and both spent their careers on artificial intelligence: Herbert Simon and Geoffrey Hinton. When Hinton won his Nobel in 2024, Carnegie Mellon noted he was only the second person to manage it. The first was their own Herbert Simon, back in 1978.

The interesting part is not how rare this is. It is who the two are.

<div class="synapse-watch" style="max-width:320px;margin:2rem auto;">
  <div style="position:relative;padding-bottom:177.78%;height:0;overflow:hidden;border-radius:12px;">
    <iframe src="https://www.youtube-nocookie.com/embed/bTwMYVWyV1s" title="Only two people won both a Turing Award and a Nobel — a Midweek Synapse Short" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" style="position:absolute;top:0;left:0;width:100%;height:100%;border:0;"></iframe>
  </div>
  <p style="text-align:center;margin:.6rem 0 0;font-size:.9rem;"><em>The 53-second version. Watch on <a href="https://www.youtube.com/shorts/bTwMYVWyV1s">YouTube</a>.</em></p>
</div>

<img src="/assets/synapse/herbert-simon.webp" alt="Black-and-white photographic portrait of Herbert Simon smiling slightly, in a suit and tie." style="max-width:min(100%,420px);height:auto;display:block;margin:0 auto;">

*Herbert Simon. Rochester Institute of Technology, via Wikimedia Commons (public domain).*

Simon won the 1975 Turing Award, with Allen Newell, for founding "symbolic" AI: the idea that you could build intelligence out of symbols and hand-written rules, like one enormous, careful logic machine. Three years later he won the Nobel in economics for a very different-sounding result. Real people, he showed, do not make perfectly optimal decisions. They cannot weigh every option, so they search until something is good enough, and stop.

<img src="/assets/synapse/hinton-nobel-2024.webp" alt="Geoffrey Hinton standing at a wooden lectern bearing the Royal Swedish Academy of Sciences sign, delivering a lecture against a dark stage." style="max-width:100%;height:auto;">

*Geoffrey Hinton at the 2024 Nobel lectures in Stockholm, the week he became the second person to hold both prizes. Jay Dixit, Wikimedia Commons, CC BY-SA 4.0.*

Hinton won the 2018 Turing Award for neural networks, the approach that eventually beat Simon's and now runs modern AI. His 2024 Nobel was for the physics underneath them: systems that learn not by following rules, but by slowly settling into a stable, low-energy state, the way a ball rolls to the bottom of a bowl.

So the only two people to bridge computing and the Nobel are the flag-bearers of AI's two rival camps: rules versus learning. And Simon's camp is the one Hinton's is usually said to have beaten.

## The neat story falls apart on one word

Here is the tempting version. Simon's Nobel says humans do not optimise. Hinton's Nobel is for machines that do. The champion of rules proved people are not perfect maximisers; the champion of learning built machines that are. A clean reversal.

It falls apart on the word "optimise," which means finding the single best answer.

Hinton's machines do not find the best answer. They roll downhill to a resting spot that is good enough, not the lowest one possible. One of his famous designs, the Boltzmann machine, even adds a little deliberate randomness, so the system can shake itself out of a bad resting spot and keep looking. And the everyday workhorse of modern AI, gradient descent, makes no promise of a perfect answer at all. It takes small steps downhill and stops when it runs out of time.

That is not "find the perfect answer." It is "search sensibly when you cannot possibly check everything." Which is almost exactly Simon's idea. He even named it in 1976: being rational means searching well under limits, not reaching the best outcome there is.

<img src="/assets/synapse/turing-nobel-convergence.svg" alt="Two columns. Herbert Simon, Turing Award 1975 and Nobel 1978, standard-bearer of symbolic AI and bounded rationality. Geoffrey Hinton, Turing Award 2018 and Nobel 2024, standard-bearer of connectionism and the Boltzmann machine. The two are usually cast as rivals, but arrows from both converge on a single box reading: Intelligence is search under limits. A caption notes they differ only on what the search space is made of, discrete symbols or continuous weights." style="max-width:100%;height:auto;">

*Cast as rivals, but both land on the same claim: intelligence is search under limits.*

## They agree more than they disagree

Simon's founding claim was that intelligence is a search through far too many possibilities to ever check them all. A neural network is a search through far too many number settings to ever check them all. Different machinery, same belief: intelligence is search under limits.

Their real disagreement is narrower than the textbooks make it sound. It is about what you are searching through: Simon's tidy symbols and rules, or the millions of adjustable numbers a neural network learns from examples. That is a genuine argument. It is just much smaller than "each proved the other wrong."

The two camps are not identical, to be fair. A neural network at least has a fixed target to move toward; Simon's human decision-maker has none. But neither one reaches a perfect answer, and both treat intelligence as a search rather than a flawless calculation. Underneath seventy years of paradigm war, the two people the Nobel and Turing committees both singled out were making nearly the same claim about what intelligence is.

## Sources

- Simon's Turing Award citation, for founding symbolic AI with Allen Newell: [ACM A.M. Turing Award](https://amturing.acm.org/award_winners/simon_1031467.cfm).
- Simon's 1978 Nobel, for bounded rationality in economic organisations: [NobelPrize.org](https://www.nobelprize.org/prizes/economic-sciences/1978/simon/facts/).
- Hinton and Hopfield's 2024 Physics Nobel, for the network machinery that learns by settling into low-energy states: [NobelPrize.org press release](https://www.nobelprize.org/prizes/physics/2024/press-release/).
- Hinton named as the second-ever laureate to hold both, after Simon: [Carnegie Mellon University](https://www.cmu.edu/news/stories/archives/2024/october/former-cmu-faculty-geoffrey-hinton-awarded-2024-nobel-prize-in-physics).

Part of #MidweekSynapse, my weekly quest to learn in public.
