"""Train the electronic noses.

1. Sample nose: sniff each of the six curated smells 200 times -> random forest names the smell.
2. Profile nose: sniff random mixtures built from ANY of the dataset's smell words
   -> random forest predicts the smell-word profile (so it can describe any smell).
"""
import os

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split

import sensor
import smell_model

HERE = os.path.dirname(os.path.abspath(__file__))
NOSE_PATH = os.path.join(HERE, "nose.joblib")
PROFILE_PATH = os.path.join(HERE, "nose_profile.joblib")
N_PROFILE_SNIFFS = 6000
PROFILE_RF = dict(n_estimators=100, min_samples_leaf=10, n_jobs=-1, random_state=0)   # lean, for free hosting
TOP = 5


def train_sample_nose():
    samples = sensor.load_samples()
    rng = np.random.default_rng(0)
    X, y = [], []
    for name, info in samples.items():
        smiles = list(info["molecules"].values())
        for _ in range(200):
            X.append(sensor.sniff(smiles, rng))
            y.append(name)
    X, y = np.array(X), np.array(y)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=0)
    clf = RandomForestClassifier(n_estimators=200, n_jobs=-1, random_state=0).fit(Xtr, ytr)
    acc = clf.score(Xte, yte)
    print(f"Sample nose accuracy on new sniffs: {acc:.1%}")
    joblib.dump({"clf": clf, "acc": acc}, NOSE_PATH, compress=3)


def make_profile_data(n, seed, max_words=2):
    """n simulated sniffs of mixtures built from 1..max_words smell words."""
    labels = smell_model._load()["labels"]
    usable = [w for w in labels if len(smell_model.word_pool(w)) >= 8]
    rng = np.random.default_rng(seed)
    X, Y, intended = [], [], []
    for _ in range(n):
        words = list(rng.choice(usable, size=rng.integers(1, max_words + 1), replace=False))
        pool = sorted({s for w in words for s in smell_model.word_pool(w)})
        smiles = [pool[i] for i in rng.choice(len(pool), size=min(6, len(pool)), replace=False)]
        X.append(sensor.sniff(smiles, rng))
        Y.append(np.mean([smell_model.label_vector(s) for s in smiles], axis=0))
        intended.append([labels.index(w) for w in words])
    return np.array(X), np.array(Y), intended, labels, usable


def train_profile_nose():
    X, Y, intended, labels, usable = make_profile_data(N_PROFILE_SNIFFS, seed=1)
    idx = np.arange(len(X))
    tr, te = train_test_split(idx, test_size=0.2, random_state=0)
    reg = RandomForestRegressor(**PROFILE_RF).fit(X[tr], Y[tr])
    pred = reg.predict(X[te])
    hits = [any(j in np.argsort(p)[::-1][:TOP] for j in intended[i]) for p, i in zip(pred, te)]
    hit = float(np.mean(hits))
    chance = TOP / len(labels)
    print(f"Profile nose: intended smell word in its top {TOP} guesses "
          f"{hit:.1%} of new sniffs (random guessing ~{chance:.1%})")
    reg.fit(X, Y)
    joblib.dump({"reg": reg, "labels": labels, "hit": hit, "usable": usable}, PROFILE_PATH, compress=3)


def main():
    train_sample_nose()
    train_profile_nose()
    print("Saved noses.")


if __name__ == "__main__":
    main()
