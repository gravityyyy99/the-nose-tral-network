# Training the nose

*Teaching the nose is the hard part. With only eight numbers per sniff, it has to tell dozens of similar smells apart. Here is how it learned, and how we checked it was not fooling us.*

The nose model learns to turn 8 sensor numbers into smell words. There are actually two versions in the project, trained by `train_nose.py`.

## Version 1: the six-smell nose

The simple version recognises the six hand-written smells.

1. Sniff each smell **200 times** (with fresh noise and humidity every time). That gives 1,200 sniffs.
2. Split them 80% for training and 20% for testing, keeping the six smells balanced.
3. Train a **random forest classifier** (200 trees) to name the smell from the 8 numbers.

Accuracy on the held-back sniffs: about **98%** in the last training run (the exact figure varies a little each time you train).

This number is high because the test sniffs come from the same simulator as the training sniffs. A real sensor would be harder.

## Version 2: the any-smell nose (used in the app)

Naming one of six smells is limited. The app lets you type any of 138 words, so the main nose is trained differently.

1. Create **6,000 simulated sniffs**. For each one:
   - choose 1 or 2 smell words at random,
   - pick 6 molecules that carry them,
   - run the sensor simulation to get 8 numbers.
2. The **target** for each sniff is the average smell-word profile of the molecules that were used: a list of 138 scores.
3. Train a **random forest regressor** (100 trees) to predict that 138-score profile from the 8 numbers.

In the app, the five highest-scoring words become "the nose's guess".

## How we measured it

On sniffs the model never saw:

| Test | Result | Pure guessing |
|---|---|---|
| Intended word is the nose's **best** guess | {{top1}} | {{c1}} |
| Intended word is in the nose's **top 5** guesses | {{top5}} | {{c5}} |

The evaluation script (`evaluate.py`) trains on one set of sniffs and tests on a different set made with a different random seed, using single-word sniffs so the intended answer is unambiguous.

## Why not higher?

- Only 8 numbers carry all the information. Many smells land in the same region of the 8-number space.
- Words that mean similar things (*fruity*, *sweet*, *tropical*) overlap strongly.
- Words with few or inconsistent molecules (*tea*, *celery*) have almost no signal.

The nose is far better than chance, but it is not a perfect smeller. The next chapters show exactly where it works and where it does not.

> **The takeaway.** Testing on sniffs the model never saw is what makes the {{top5}} figure trustworthy. The number is modest, and it is honest.
