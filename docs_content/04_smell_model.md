# The smell model

*How do you teach a computer what vanilla smells like without ever letting it smell anything? You show it the shapes of molecules and let it find the pattern.*

The smell model answers one question: **given a molecule, which smell words describe it?**

## Step 1: turn a molecule into numbers

A model cannot read a drawing of a molecule, so each molecule is turned into a **fingerprint**: a list of 2,048 numbers.

The method is called a **Morgan fingerprint** (also known as ECFP), computed with the RDKit chemistry library:

1. For each atom, look at the atom and its neighbours up to 2 bonds away. That small neighbourhood is a "fragment".
2. Give each distinct fragment a position among the 2,048 slots.
3. Count how many times each fragment appears.

The result is a row of counts saying "this molecule has 3 of fragment A, 1 of fragment B, and none of the rest". Molecules that share fragments get similar fingerprints.

## Step 2: learn which fragments go with which words

The model is a **random forest** with 200 trees, from scikit-learn.

A decision tree asks a chain of yes/no questions, like "does fragment 412 appear?", until it reaches an answer. A random forest builds many trees on slightly different views of the data and averages their answers. It is robust and needs very little tuning.

The forest is trained for all 138 words at once, so for each molecule it outputs 138 scores between 0 and 1.

## Step 3: test it honestly

To test the model fairly, the data is split:

- **80%** (3,986 molecules) used for training
- **20%** (997 molecules) held back and never shown during training

The model then predicts the held-back molecules and its answers are compared with the experts' labels.

### The accuracy measure: ROC-AUC

For each smell word, ROC-AUC asks: *if I pick one molecule that really has this word and one that does not, how often does the model give the right one the higher score?*

- **0.5** means pure guessing
- **1.0** means perfect

The result, averaged over words, is **{{auc}}**. For a reference, the paper's authors report 0.89 with their more advanced graph neural network.

## Step 4: use it

After testing, the model is trained again on all the data so the app uses everything available. To describe a mixture, the app asks the model about each molecule and averages the scores. The top words are what you see in the "Smell model" panel.

## What the smell model cannot do

- It has never smelled anything. It only learned from expert labels.
- It works on molecules, not on sensor readings. That is the nose model's job (next chapters).
- Words that experts disagree on, like *tea* or *weedy*, score near guessing.

## An intuition for how it learns

Take isoamyl acetate, the molecule behind the smell of banana. Its structure contains an *ester* group, a particular cluster of carbon and oxygen atoms. Across the dataset, many molecules that contain ester groups were labelled *fruity* by the experts. The fingerprint records that the fragment is present, and the forest learns that molecules with that fragment are often fruity. It does this for thousands of fragments at once, and combines the evidence.

No one told the model that esters smell fruity. It worked that out from the examples.

> **The takeaway.** The smell model turns chemistry into numbers, learns from experts, and scores {{auc}} on molecules it has never seen. It is a solid base, not a perfect one.
