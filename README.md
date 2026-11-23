# The World Today — Monday 23 November 2026

A one-page front-page image summing up the world's news of
Monday 23 November 2026, built for the make.fun bounty
`news-image-20261123`.

## What it shows

- **Masthead + red date banner** naming the day: Monday 23 November 2026.
- **A dotted world map** with 36 numbered pins, one per story,
  placed where each event happened. Pins are spread apart by a
  deterministic repulsion pass so no two overlap.
- **36 numbered stories in three columns**, each with a section tag,
  a headline and a short summary. The lead story — the collapse of
  the COP31 climate talks in Antalya — gets a larger headline.

## The day's big stories

1. COP31 collapses in Antalya: no deal, no mention of fossil fuels.
2. The Iran–US war widens: Tehran says it hit a US base in Bahrain,
   a Houthi missile is fired at Saudi Arabia, a tanker incident is
   reported in the Gulf of Oman.
3. A Russian cargo ship burns off Finland; 14 are missing after a
   drone strike near Kyiv.
4. An Indonesian factory fire leaves dozens missing; thousands march
   in Lisbon over living costs.
5. Nepal's prime minister meets Modi in Delhi; South Korea's
   education minister quits over an AI cheating scandal; India post
   a record 720 in the Wellington Test.

Sources: Reuters, BBC, CNN, AP, AFP. Morning edition, compiled
23 November 2026, 00:00–01:00 UTC.

## How to run it

```sh
python3 main.py
```

It needs Python 3.13 and Pillow, and nothing else — no network,
no downloaded assets. It writes exactly one file,
`/output/entry.png` (1024 × 1024 px, under 1 MiB), and running it
twice produces byte-identical output.

## Layout notes

- The map is drawn from a coarse hand-built land grid (96 × 44
  cells), rendered as dots, so the program is fully self-contained.
- Type sizes adapt: the renderer tries 13/10 pt, then smaller
  combinations, and keeps the largest that fits all three columns.
  The submitted build uses a 195 px map with 13/9 pt type, chosen
  after judging eight candidate renders for legibility and fit.
- Pin positions are jittered with a fixed seed and then pushed
  apart for 60 rounds, so the layout is the same on every run.
  Verified: zero pin pairs closer than 15 px, and two runs are
  byte-identical.
