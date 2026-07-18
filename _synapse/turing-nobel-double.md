---
title: "Only two people have won both a Turing Award and a Nobel Prize"
date: 2026-07-12
synapse: 3
tags: [artificial-intelligence, history-of-ai, bounded-rationality, deep-learning]
excerpt: "Both are AI researchers, on opposite sides of the field's oldest argument. The neat story is that each disproved the other. I went to check, and the neat story is wrong."
---

This one started as a tidy fact I wanted to post, and turned into a small lesson about tidy facts.

My notes had a candidate line: "exactly one person has ever won both computer science's Turing Award and an actual Nobel Prize." That person was Herbert Simon. I went to confirm it before writing anything, and the number had quietly changed underneath the note.

## The count is two now

Geoffrey Hinton won the 2018 Turing Award for deep learning, and in 2024 he won the Nobel Prize in Physics with John Hopfield. That makes two. Carnegie Mellon, announcing Hinton's Nobel, said so directly: he is the second person to hold both, and the first was their own Herb Simon.

Two is somehow a better number than one, because of *who* the two are.

Simon won his Turing Award in 1975, with Allen Newell, for founding symbolic AI: the idea that a machine shuffling symbols according to rules has everything it needs for intelligence. He won his Nobel three years later for bounded rationality, the argument that real decision-makers cannot optimise and instead search until something is good enough.

Hinton won his Turing Award for the neural networks that displaced Simon's whole paradigm, and his Nobel for the physics underneath them: networks that learn not by applying rules to symbols, but by settling into low-energy states.

So the only two people who ever bridged computing and the Nobel committee are the standard-bearers of the two theories of mind that AI has spent seventy years choosing between. Symbolic versus connectionist. Rules versus learned weights. Simon's side is the one Hinton's work is usually said to have beaten.

That is where the tidy version wants to end, and it is a genuinely tempting ending.

## The tempting symmetry, and why it breaks

Here is the neat story. The symbolist won his Nobel for showing that humans do *not* optimise. The connectionist won his Nobel for machines whose entire learning method *is* optimisation. The champion of rules proved people are not tidy maximisers; the champion of learning built machines that are. A perfect reversal.

I really wanted that to be true. It is not, and the reason it is not is the actually interesting part.

The word "optimisation" is doing two different jobs. Hinton's machines do not find the best answer. A Hopfield network is guaranteed only to slide into the *nearest* low point, not the lowest. The Boltzmann machine exists precisely *because* that is a problem: Hinton and Terry Sejnowski added a dose of controlled randomness, borrowed from metallurgy, specifically to let the network jump out of poor solutions while it searches. And plain gradient descent, the workhorse of modern AI, makes no claim to find a global best at all. It is local, greedy, iterative, a little random, and it stops when the compute budget runs out.

That is not the "optimise everything" that Simon spent his career attacking. It is closer to the opposite. Simon even gave it a name in a 1976 paper: procedural rationality, where a process counts as rational because it is a sensible way to search under limits, not because it reaches the maximum.

Which flips the whole picture.

<img src="/assets/synapse/turing-nobel-convergence.svg" alt="Two columns. Herbert Simon, Turing Award 1975 and Nobel 1978, standard-bearer of symbolic AI and bounded rationality. Geoffrey Hinton, Turing Award 2018 and Nobel 2024, standard-bearer of connectionism and the Boltzmann machine. The two are usually cast as rivals, but arrows from both converge on a single box reading: Intelligence is search under limits. A caption notes they differ only on what the search space is made of, discrete symbols or continuous weights." style="max-width:100%;height:auto;">

*The rivalry is real, but it is narrower than the paradigm-war framing suggests.*

## They agree more than they disagree

Hinton's machines are not a refutation of Simon's idea. They are an example of it.

Newell and Simon's founding claim was that intelligence is search through a space far too large to ever enumerate. Gradient descent is search through a space of weights far too large to ever enumerate. Both laureates are committed to the same thing: intelligence is search under limits. They disagree about what the search space is made of, discrete symbols or continuous weights, and about whether the representations are handwritten or learned. That is a real quarrel. It is just a much smaller one than "each disproved the other."

I want to be honest about the seams, because forcing a second neat symmetry would repeat the mistake I just made. Simon's satisficing has a specific mechanism, an aspiration level you stop at; gradient descent has no aspiration level. Neural networks *do* have a clean objective function; Simon's human decision-maker does not. Having an objective is not the same as reaching its maximum, but the difference is real and I am not going to paper over it. And whether "connectionism won" is even the right verdict is itself a live argument.

The lesson I took is smaller than the AI history and more useful to me. A hook that is too neat is not a gift. It is a fact-check prompt. The true finding here needed a paragraph where the false one needed a sentence, and it was worth the extra paragraph.

## Sources

- Simon's Turing Award citation, for founding symbolic AI with Allen Newell: [ACM A.M. Turing Award](https://amturing.acm.org/award_winners/simon_1031467.cfm).
- Simon's 1978 Nobel, for bounded rationality in economic organisations: [NobelPrize.org](https://www.nobelprize.org/prizes/economic-sciences/1978/simon/facts/).
- Hinton and Hopfield's 2024 Physics Nobel, for the network machinery that learns by settling into low-energy states: [NobelPrize.org press release](https://www.nobelprize.org/prizes/physics/2024/press-release/).
- Hinton named as the second-ever laureate to hold both, after Simon: [Carnegie Mellon University](https://www.cmu.edu/news/stories/archives/2024/october/former-cmu-faculty-geoffrey-hinton-awarded-2024-nobel-prize-in-physics).

Part of #MidweekSynapse, my weekly quest to learn in public.
