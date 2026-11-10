"""Simulated electronic nose: 8 gas-sensor channels.

Each channel is tuned to one property of a molecule (size, oil-loving-ness,
oxygen, sulfur, aromatic rings) with a little cross-sensitivity, like real
metal-oxide sensors. Swap this file for real BME688 readings (README Part 3).
"""
import functools
import json
import os

import numpy as np
from rdkit import Chem
from rdkit.Chem import Crippen, Descriptors

HERE = os.path.dirname(os.path.abspath(__file__))
N_SENSORS = 8

# (name shown to people, what it reacts to)
CHANNEL_INFO = [
    ("Small and light", "small, very volatile molecules"),
    ("Large and heavy", "big, slower-evaporating molecules"),
    ("Oily / fatty", "oil-loving molecules such as terpenes and hydrocarbons"),
    ("Water-loving", "polar molecules such as acids and alcohols"),
    ("Oxygen-rich", "aldehydes, ketones and esters (fruity, sweet notes)"),
    ("Sulfur", "sulfur compounds (coffee, onion, garlic)"),
    ("Aromatic rings", "ring compounds such as phenols and vanillin"),
    ("General gases", "a broad response to almost any smell"),
]
CHANNELS = [name for name, _ in CHANNEL_INFO]

# weights over [size, oil-loving, oxygen, sulfur, aromatic]
_W = np.zeros((N_SENSORS, 5))
_W[0, 0], _W[1, 0] = -1.5, 1.5
_W[2, 1], _W[3, 1] = 1.5, -1.5
_W[4, 2] = 1.5
_W[5, 3] = 1.5
_W[6, 4] = 1.5
_W[7, :] = 0.5
_W += np.random.default_rng(42).normal(0, 0.35, _W.shape)   # cross-sensitivity


def load_samples():
    with open(os.path.join(HERE, "samples.json"), encoding="utf-8") as f:
        return json.load(f)


@functools.lru_cache(maxsize=None)
def molecule_features(smiles):
    mol = Chem.MolFromSmiles(smiles)
    size = (Descriptors.MolWt(mol) - 140.0) / 60.0
    logp = (Crippen.MolLogP(mol) - 2.0) / 1.5
    n_o = sum(a.GetSymbol() == "O" for a in mol.GetAtoms()) - 1.0
    n_s = 2.0 * sum(a.GetSymbol() == "S" for a in mol.GetAtoms())
    arom = (sum(a.GetIsAromatic() for a in mol.GetAtoms()) / 6.0 - 0.5) * 2.0
    return np.array([size, logp, n_o, n_s, arom])


def sniff(smiles_list, rng, noise=0.08):
    """One noisy sniff of a mixture -> 8 sensor readings (about -1 to +1)."""
    feats = np.array([molecule_features(s) for s in smiles_list])
    conc = rng.uniform(0.3, 1.0, len(feats))     # random concentration of each molecule
    conc /= conc.sum()
    clean = np.tanh(feats @ _W.T)                # (molecules, sensors)
    reading = (conc[:, None] * clean).sum(axis=0)
    humidity = rng.uniform(0.0, 1.0)             # humidity nudges some sensors
    reading = reading + humidity * np.linspace(0.15, -0.05, N_SENSORS)
    gain = rng.normal(1.0, 0.05)                 # sensor drift
    return reading * gain + rng.normal(0, noise, N_SENSORS)


def to_percent(reading):
    """Map a raw reading (about -1..+1) to a 0-100 'reaction strength' for display."""
    return np.clip((np.asarray(reading) + 1.0) / 2.0 * 100.0, 0, 100)
