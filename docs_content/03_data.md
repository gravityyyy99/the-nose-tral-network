# The data

*Every AI is only as good as what it learned from. This chapter opens the textbook that Aroma-GPT studied.*

Every model needs examples to learn from. This project uses one dataset for the smell model, and a small hand-written file for the curated sample smells.

## The OpenPOM dataset

The data comes from the **OpenPOM** project, an open-source rebuild of the Google smell research. The file is `curated_GS_LF_merged_4983.csv`.

| Fact | Value |
|---|---|
| Molecules | 4,983 |
| Smell words (labels) | 138 |
| Source of the labels | The Good Scents Company and Leffingwell (two fragrance-industry databases), merged and cleaned by OpenPOM |
| Who labelled them | Perfume and flavour experts |

Each row is one molecule. It has:

- the molecule written as text (a SMILES string, explained below)
- a list of smell words, such as `fruity;sweet;green`
- 138 columns of 0 or 1, one per smell word, saying whether that word applies

## What is a SMILES string?

SMILES is a way of writing a molecule as a line of text. For example:

| Text | Molecule |
|---|---|
| `CC(C)CCOC(C)=O` | isoamyl acetate, the main "banana" smell |
| `COc1cc(C=O)ccc1O` | vanillin, the main "vanilla" smell |
| `CC(C)C1CCC(C)CC1O` | menthol, the "mint" smell |

Letters are atoms (C is carbon, O is oxygen, S is sulfur). Brackets show branches, `=` shows double bonds, and lowercase letters show atoms in rings.

## Multi-label data

One molecule can have several smell words at once. Vanillin is *sweet*, *vanilla* and *creamy* together. So the model does not pick one answer. It predicts a score for all 138 words at the same time. This is called **multi-label classification**.

## The six hand-written samples

`samples.json` contains six everyday smells, each as a list of the real aroma molecules found in it: coffee, vanilla candle, mint, lemon, banana and wood smoke. For example the banana entry lists isoamyl acetate, isoamyl butyrate, ethyl butyrate, hexyl acetate and butyl acetate.

These make the demo recognisable. They are used for the "six smells" nose and when you type one of those exact names.

## Picking molecules for any smell word

For the other 138 words, the app needs molecules that carry that smell. For each word, the program takes the molecules labelled with it and keeps the **25 "purest"**, meaning the ones with the fewest other smell labels. Each sniff then draws 6 of them at random. This keeps a *woody* sniff from being full of molecules that are mostly something else.

## Honest limits of the data

- Labels come from human opinion, which varies between experts.
- Some words are vague (*tea*, *weedy*, *warm*) and the model finds them hard.
- Mixtures in real life contain hundreds of molecules, not 6.

> **Did you know?** A well-known 2014 study estimated that people can tell apart more than a trillion different smells. Later researchers disputed that number. Either way, the space of possible smells is enormous, which is exactly why a model that learns from examples is useful.

> **The takeaway.** Almost 5,000 molecules, 138 smell words and human experts: the data is the foundation, and its limits become the model's limits.
