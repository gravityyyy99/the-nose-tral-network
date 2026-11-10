# Credits

*No project is built alone. Here is everyone whose work made this one possible.*

**The Nose-tral Network** is a project created by **Dibyajyoti Pradhan**. The AI in it is called **Aroma-GPT**.

&copy; 2026 Dibyajyoti Pradhan. All rights reserved.

This project stands on the work of others. Thank you to everyone below.

## Research

**Lee, B. K. et al. (2023). *A principal odor map unifies diverse tasks in olfactory perception.* Science.** The research from Google Research, Osmo and the Monell Chemical Senses Center that showed a model can predict smell from molecular structure. The idea behind this project comes from this paper.

## Data and reference model

**OpenPOM** (MIT licence), the open-source rebuild of that research, and its curated dataset of 4,983 molecules labelled with 138 smell words. The data is built on the **Good Scents Company** and **Leffingwell** odour databases, whose experts labelled the molecules.

Repository: https://github.com/BioMachineLearning/openpom

## Software

| Tool | Used for |
|---|---|
| RDKit | reading molecules, fingerprints, drawing structures |
| scikit-learn | random forest models and accuracy measures |
| pandas and NumPy | data handling |
| Altair | charts |
| Streamlit | the web app |
| Python | everything |

## What is original here

- The combination of a molecule-based smell model and a sensor-based nose model in one pipeline.
- The simulated 8-sensor electronic nose, with noise, humidity and drift.
- The any-smell nose model, trained on mixtures built from the 138 smell words.
- The free-text interface with spelling correction.
- The per-word accuracy evaluation and this documentation.

## Development note

The code was written with the help of an AI coding assistant (Claude, from Anthropic), working from the project's design and direction.

## Responsible use

This is an educational demonstration. The electronic nose is simulated, and nothing here should be used for safety-critical decisions such as detecting gas leaks, spoiled food or hazardous chemicals.
