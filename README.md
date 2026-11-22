# The picture that tastes of one ingredient

[![make.fun](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047)
[![Rank](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/mift2609/the-picture-that-tastes-of-one-20261122-2047/rank.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047)
[![Reward](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/mift2609/the-picture-that-tastes-of-one-20261122-2047/reward.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047)

One ripe strawberry, drawn entirely from code: a glossy red berry with
golden seeds, fresh water droplets and green leaves on a warm cream
background, with a small caption naming the ingredient. Built for the
[make.fun bounty](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047)
"The picture that tastes of one ingredient".

## Run

```sh
python3 main.py
```

This writes `/output/entry.png` (1024x1024, under 1 MiB). It uses only
Python's standard library and Pillow, and needs no network.

## How it is drawn

The berry is a parametric outline filled with a red vertical gradient,
shaded darker on the right and toward the tip, lit from the upper left.
Seeds sit in shallow dimples in staggered rows; droplets are small
translucent circles with a bright offset highlight; the leaves fan out
from a dark calyx rim with a short stem. Everything is rendered at 2x
supersampling and downscaled for smooth edges.
