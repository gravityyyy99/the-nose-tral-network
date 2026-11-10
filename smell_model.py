"""Aroma-GPT smell model: molecule (SMILES) -> smell words.

Turns each molecule into a Morgan fingerprint (a bit-vector of chemical
fragments) and learns which fragments go with which smell words.
Run `python smell_model.py` to download the dataset and train.
"""
import os
import tempfile
import urllib.request

import joblib
import numpy as np
import pandas as pd
from rdkit import Chem, RDLogger
from rdkit.Chem import rdFingerprintGenerator
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

RDLogger.DisableLog("rdApp.*")

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "data", "curated_GS_LF_merged_4983.csv")
MODEL_PATH = os.path.join(HERE, "smell_model.joblib")
DATA_URL = ("https://raw.githubusercontent.com/BioMachineLearning/openpom/main/"
            "openpom/data/curated_datasets/curated_GS_LF_merged_4983.csv")
N_BITS = 2048
# lean forest: fewer trees and bigger leaves keep the trained model small enough for free hosting
SMELL_RF = dict(n_estimators=100, min_samples_leaf=5, n_jobs=-1, random_state=0)
_gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=N_BITS)


def fingerprint(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return _gen.GetCountFingerprintAsNumPy(mol).astype(np.float32)


def download_data():
    """Return the dataset path, downloading it once. Falls back to a temp folder if the project folder is read-only."""
    if os.path.exists(DATA_PATH):
        return DATA_PATH
    for folder in (os.path.dirname(DATA_PATH), os.path.join(tempfile.gettempdir(), "aroma-gpt-data")):
        path = os.path.join(folder, os.path.basename(DATA_PATH))
        if os.path.exists(path):
            return path
        try:
            os.makedirs(folder, exist_ok=True)
            print(f"Downloading dataset from {DATA_URL}")
            urllib.request.urlretrieve(DATA_URL, path)
            return path
        except OSError:
            continue
    raise RuntimeError("Could not save the dataset anywhere writable")


def load_dataset():
    df = pd.read_csv(download_data())
    smiles_col = df.columns[0]
    label_cols = [c for c in df.columns[1:]
                  if df[c].dropna().isin([0, 1]).all()]
    X, keep = [], []
    for i, s in enumerate(df[smiles_col]):
        fp = fingerprint(s)
        if fp is not None:
            X.append(fp)
            keep.append(i)
    X = np.vstack(X)
    Y = df.loc[keep, label_cols].fillna(0).values.astype(int)
    return X, Y, label_cols


def train():
    X, Y, labels = load_dataset()
    print(f"{X.shape[0]} molecules, {len(labels)} smell words")
    Xtr, Xte, Ytr, Yte = train_test_split(X, Y, test_size=0.2, random_state=0)
    clf = RandomForestClassifier(**SMELL_RF)
    clf.fit(Xtr, Ytr)
    probs = np.column_stack([p[:, 1] if p.shape[1] > 1 else np.zeros(len(Xte))
                             for p in clf.predict_proba(Xte)])
    aucs = [roc_auc_score(Yte[:, j], probs[:, j]) for j in range(Y.shape[1])
            if 0 < Yte[:, j].sum() < len(Yte)]
    auc = float(np.mean(aucs))
    print(f"Test ROC-AUC (mean over smell words, unseen molecules): {auc:.3f}")
    clf.fit(X, Y)  # refit on everything for the app
    joblib.dump({"clf": clf, "labels": labels, "auc": auc}, MODEL_PATH, compress=3)
    print(f"Saved {MODEL_PATH}")


_cache = {}


def _load():
    if "m" not in _cache:
        _cache["m"] = joblib.load(MODEL_PATH)
    return _cache["m"]


def predict_proba(smiles_list):
    """Mean probability of each smell word across the given molecules."""
    m = _load()
    X = np.vstack([fingerprint(s) for s in smiles_list])
    probs = np.column_stack([p[:, 1] if p.shape[1] > 1 else np.zeros(len(X))
                             for p in m["clf"].predict_proba(X)])
    return dict(zip(m["labels"], probs.mean(axis=0)))


def _table():
    if "df" not in _cache:
        df = pd.read_csv(download_data())
        labels = _load()["labels"]
        df["_n"] = df[labels].sum(axis=1)
        _cache["df"] = df
    return _cache["df"]


def word_pool(word, k=25):
    """The k 'purest' molecules for a smell word (fewest other smell labels)."""
    key = ("pool", word, k)
    if key not in _cache:
        df = _table()
        sub = df[df[word] == 1].sort_values("_n", kind="stable").head(k)
        _cache[key] = list(sub[df.columns[0]])
    return _cache[key]


def label_vector(smiles):
    """0/1 smell-word vector of a dataset molecule (None if not in dataset)."""
    if "vecs" not in _cache:
        df = _table()
        labels = _load()["labels"]
        _cache["vecs"] = {s: v for s, v in zip(df[df.columns[0]], df[labels].values.astype(float))}
    return _cache["vecs"].get(smiles)


def describe(smiles_list, top=5):
    """Top smell words for a mixture of molecules."""
    scores = predict_proba(smiles_list)
    return sorted(scores, key=scores.get, reverse=True)[:top]


if __name__ == "__main__":
    train()
