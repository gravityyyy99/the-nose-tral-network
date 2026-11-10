# Results and limits

*Every project shows its best results. This chapter shows all of them.*

This chapter reports what the models achieve, including where they fail. All numbers come from `evaluate.py` and are measured on examples the models never saw during training.

## Headline numbers

| Model | Measure | Result | Pure guessing |
|---|---|---|---|
| Smell model | average ROC-AUC across words | **{{auc}}** | 0.50 |
| Nose model | intended word is the best guess | **{{top1}}** | {{c1}} |
| Nose model | intended word is in the top 5 | **{{top5}}** | {{c5}} |
| Six-smell nose | correct smell named | about **98%** | 17% |

## What the numbers mean

- The **smell model** is genuinely useful: it ranks molecules well for most smell words.
- The **nose model** is much better than guessing, but with only 8 sensors it often confuses similar smells. Finding the right word among its top 5 guesses is its realistic strength.

## It varies a lot by smell

**Smell model, strongest words** (ROC-AUC): popcorn, cedar, clove, sulfurous, coumarinic, amber, smoky and beefy, all around 0.96 to 0.99. These have distinctive chemistry.

**Smell model, weakest words**: celery is near guessing, and fruit skin, tea, metallic and berry are not much better. Experts use these words inconsistently.

**Nose, easy words** (found in the top 5 almost every time): fruity, floral, green, woody, apple, sulfurous and ketonic.

**Nose, hard words**: lavender, celery, musty, raspberry, tea and leafy are almost never found by the nose.

Some everyday examples, copied from the last evaluation run (they can shift slightly if you retrain):

| Smell | Nose finds it in top 5 | Smell model accuracy |
|---|---|---|
| fruity | 100% | 0.83 |
| vanilla | 83% | 0.94 |
| coffee | 69% | 0.91 |
| banana | 65% | 0.91 |
| smoky | 26% | 0.96 |
| lemon | 23% | 0.82 |
| mint | 17% | 0.85 |
| lavender | 0% | 0.72 |

Notice that *smoky* is easy for the smell model (0.96) but hard for the nose (26%). The molecules are distinctive, but the 8 simulated sensors do not separate them well. That difference between the two models is the whole point of having both.

## Limits you should know about

1. **The nose is simulated.** Test sniffs come from the same simulator as training sniffs. A real sensor would give lower accuracy because of drift, temperature and other effects the simulator does not copy.
2. **Shared molecules.** The test sniffs reuse molecules from the same pool as training sniffs, with different mixtures and noise. A harder test would hold out entire molecules, so the nose numbers are somewhat optimistic.
3. **Small mixtures.** Real smells contain hundreds of molecules. Each sniff here has about 6.
4. **Random split.** The smell model's test molecules are chosen at random, so some test molecules resemble training ones. A test on completely new chemical families would score lower.
5. **Human labels.** The dataset records expert opinion, which is partly subjective.
6. **It is a demonstration.** It shows how the full pipeline fits together, not a finished product.

## The charts

The charts below show the full spread across all smell words.

> **The takeaway.** Strong on distinctive smells, weak on vague ones, and always simulated for now. Knowing where it fails is as useful as knowing where it works.
