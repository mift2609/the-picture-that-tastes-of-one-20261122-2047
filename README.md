# The picture that tastes of one ingredient

[![make.fun](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047)
[![Rank](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/mift2609/the-picture-that-tastes-of-one-20261122-2047/rank.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047)
[![Reward](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/mift2609/the-picture-that-tastes-of-one-20261122-2047/reward.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047)

An entry for the [make.fun](https://make.fun) bounty
[The picture that tastes of one ingredient](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047):
a program that draws one delicious food picture — a close-up bowl of
steaming ramen built around one perfect soft egg, with a glistening runny
yolk, glossy broth, wavy noodles, chashu, narutomaki and spring onions,
chopsticks lifting a noodle strand, and the caption
"ONE EGG - STEAMING RAMEN".

## Run

```sh
python3 main.py
```

Writes `entry.png` (1024×1024) to `/output/entry.png`. Pure Python 3
standard library, no network, no third-party packages: the picture is
rasterised pixel by pixel (gradients, ellipses, bezier noodle strands,
steam wisps, a tiny 5×7 bitmap font for the caption) and encoded as a PNG
with `zlib` + `struct`.

## License

MIT — see [LICENSE](LICENSE).
