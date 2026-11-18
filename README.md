# news-image-20261118
[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Wangzinan62/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Wangzinan62/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image that sums up the world news of Wednesday 18 November 2026: a classic broadsheet front page with the date set huge, a lead story on the APEC summit opening in Shenzhen (with the Quad in Manila and the first US–China–Russia trilateral to follow), and panels on Nvidia's earnings, Ukraine's second strike on the Crimean Bridge, Cyclone Akvan bearing down on India, Voyager 1 nearing one light-day from Earth, and Dhoni's IPL retirement — plus an "also today" ticker along the foot of the page.

The page is drawn entirely by `build_image.py` (Python 3 + PIL): every headline, deck and illustration is a vector shape or real font glyph measured with PIL's text metrics, so nothing can come out garbled. The committed result is `entry.png` (1024×1024).

## Run it

```
MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node, standard library only) copies the committed `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`) and logs its byte size. To redraw the page from source, run `python3 build_image.py`.

<sub>Entered on [make.fun](https://make.fun/?ref=7n4st51n&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
