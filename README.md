# The MathematiCat Math Game

A single-page proof puzzle game. You are given an olympiad problem, you write a
proof, and a cat with a wooden ruler tells you where it breaks.

**Play it: https://peachpearorange.github.io/mathematicat/**

The cat marks your argument on its own merits rather than against a reference
solution, so a completely different but sound proof is fully correct. When
something is wrong it says where the argument stops being justified and what is
missing, and then stops: it will not hand you the rest. The key idea is behind a
button for when you actually want it.

## Problems

1000 of them, grouped by source, which is a rough proxy for difficulty, and
ordered from gentlest to hardest in the picker.

| Group | Count | |
|---|---|---|
| Warm-ups | 49 | written for this game, BMO1 territory |
| National olympiads | 400 | Austria, Brazil, Croatia, Estonia, Ireland, and more |
| Regional international | 250 | Baltic Way, Balkan, Nordic, Benelux, EGMO, APMO |
| Harder national traditions | 100 | Romania, China, Iran, Russia, and others |
| IMO and IMO Shortlist | 63 | |
| Olympiad by topic | 151 | algebra, number theory, combinatorics |

Geometry is excluded throughout, because the page cannot show you a diagram.
Which problems you have solved is remembered in your browser, keyed by a hash of
the problem statement, so editing the bank does not orphan your history.

## Credits

Problems and solution sketches come from two openly licensed collections, both
reformatted for this page:

- [MathNet](https://mathnet.mit.edu/) (Alshammari et al.), used under CC BY 4.0
- [OlympiadBench](https://huggingface.co/datasets/Hothan/OlympiadBench), used
  under Apache 2.0

The warm-up problems are original. Grading runs on
[OpenRouter](https://openrouter.ai/).

## Running it

Open `index.html`. That is the whole thing: one file, no build step, no server.
The API key in it is deliberately not written in a form automated harvesters can
match, which is scraper avoidance and nothing more, since anyone can read it out
of the network tab. Regenerate it with `mask_key.py` after rotating.
