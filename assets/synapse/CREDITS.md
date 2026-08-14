# /synapse image credits

Every image on the Synapse posts is public domain or self-made. No exceptions (see the
publishing rule: self-made or properly-licensed only, never textbook figures or paywalled
screenshots).

**Hero images** live in `assets/heroes/`, one per post plus three for the landing pages, and
each doubles as that page's `og:image` so a share card never falls back to nothing. They are
built by `tools/gen-assets.py`, which also renders the favicon set — run `make assets` after
adding a post. Two kinds:

- **`<slug>.jpg`** — the post's own lead photo, cropped to the hero aspect and re-encoded to
  JPEG (LinkedIn's crawler does not reliably render the WebP originals). Same source, same
  licence as the in-post image; see the table below. Which post uses which is the
  `PHOTO_HEROES` map in the script.
- **`<slug>.png`** — generated abstract art, own work, for posts whose imagery is diagrams or
  portraits that crop badly to a banner. Colour is derived from the post slug unless the post
  sets `hero_hue:` in its frontmatter.

| File | Subject | Source | License |
|---|---|---|---|
| reef.jpg | Australian coast / Great Barrier Reef from orbit | NASA Goddard | PD (NASA) |
| crater-lake.jpg | Crater Lake in winter | US National Park Service | PD (US Gov) |
| hokusai-wave.jpg | The Great Wave off Kanagawa, c. 1831 | Katsushika Hokusai | PD (age) |
| lost-city.jpg | Lost City hydrothermal chimneys | NOAA Photo Library (expl1169) | PD (NOAA) |
| enceladus-plume.jpg | Enceladus backlit plumes along the tiger stripes, "Bursting at the Seams" (PIA11688) | NASA/JPL-Caltech, Cassini | PD (NASA) — **corrected 2026-07-23**: previously this file actually held PIA06443, an ice-grain-size spectral plot mislabeled "Enceladus Plume," not a photo at all. Shared with the #4 post, so that post picked up the same fix automatically. |
| enceladus-prediction-timeline.svg | 1993 prediction → 2000/2017 confirmations timeline | self-made | own work |
| culture-iceberg-two-directions.svg | one culture iceberg read in two opposite directions (anthropology vs marketing) | self-made | own work |
| turing-nobel-convergence.svg | Simon and Hinton, two paradigms converging on "search under limits" | self-made | own work |
| iceberg-underside.webp | Arctic iceberg with underside exposed | AWeith, Wikimedia Commons ("Iceberg in the Arctic with its underside exposed") | CC BY-SA 4.0 |
| herbert-simon.webp | Herbert Simon, photographic portrait | Rochester Institute of Technology, Wikimedia Commons ("Herbert Simon close-up (cropped)") | PD (RIT/no notice) |
| hinton-nobel-2024.webp | Geoffrey Hinton at the 2024 Nobel lectures | Jay Dixit, Wikimedia Commons ("Geoffrey Hinton at the 2024 Nobel Lectures") | CC BY-SA 4.0 |
| enceladus-tiger-stripes.webp | Close-up of the tiger stripe fractures themselves, July 14 2005 flyby (PIA06247, "Tiger Stripes Up Close") | NASA/JPL-Caltech, Cassini | PD (NASA) |
| two-reframed-one-open.svg | Three questions about what life needs, tested against Enceladus: two reframed, one an open question (ocean age) | self-made | own work |
| three-theories-llm-test.svg | Three theories of disruption (Schumpeter, Christensen, Marketing/Rogers) tested against the frontier LLM: fits, doesn't fit, fits | self-made | own work |
| gpu-useful-life-divergence.svg | Assumed server useful life at Microsoft, Alphabet, Amazon and Meta, 2022 to 2026, showing the 1 Jan 2025 fork where Amazon shortened and Meta lengthened. Every value read directly from the firm's own 10-K | self-made | own work |
| dating-isotope-halflives.svg | Half-lives of the five parent isotopes used for dating, on a log scale, split by which field uses which. Values from the NPS half-life table, except potassium-40 which uses the current 1.248 Bya figure rather than the older 1.31 carried by the textbook | self-made | own work |
| apollo11-two-answers.svg | The two Apollo 11 ages published in 1970 (crystalline rocks at 3.65 Bya by Rb-Sr, soil and breccia at 4.6 to 4.66 Bya) plotted against the 4.567 Bya age of the solar system, which the soil ages exceed | self-made | own work |

Originals and their full provenance live with the video episodes in `~/Works/synapse-video/episodes/*/PROVENANCE.md`.
