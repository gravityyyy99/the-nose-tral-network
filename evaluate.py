"""Measure how accurate Aroma-GPT is, per smell word. Writes evaluation.json.

Run: python evaluate.py   (takes a minute or two)
"""
import json
import os

import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

import smell_model
from train_nose import make_profile_data

HERE = os.path.dirname(os.path.abspath(__file__))
TOP = 5


def smell_model_per_word():
    X, Y, labels = smell_model.load_dataset()
    Xtr, Xte, Ytr, Yte = train_test_split(X, Y, test_size=0.2, random_state=0)
    clf = RandomForestClassifier(n_estimators=200, n_jobs=-1, random_state=0).fit(Xtr, Ytr)
    probs = np.column_stack([p[:, 1] if p.shape[1] > 1 else np.zeros(len(Xte))
                             for p in clf.predict_proba(Xte)])
    out = {}
    for j, w in enumerate(labels):
        if 0 < Yte[:, j].sum() < len(Yte):
            out[w] = float(roc_auc_score(Yte[:, j], probs[:, j]))
    return out


def nose_per_word():
    """Train on one set of sniffs, test on a different set (new random mixtures + noise).
    Single-word sniffs only, so 'intended word' is unambiguous."""
    Xtr, Ytr, _, labels, usable = make_profile_data(6000, seed=1)
    reg = RandomForestRegressor(n_estimators=150, min_samples_leaf=3, n_jobs=-1,
                                random_state=0).fit(Xtr, Ytr)
    Xte, _, intended, _, _ = make_profile_data(len(usable) * 25, seed=99, max_words=1)
    pred = reg.predict(Xte)
    top1, top5 = {}, {}
    for p, ints in zip(pred, intended):
        w = labels[ints[0]]
        order = np.argsort(p)[::-1]
        top1.setdefault(w, []).append(order[0] == ints[0])
        top5.setdefault(w, []).append(ints[0] in order[:TOP])
    return ({w: float(np.mean(v)) for w, v in top1.items()},
            {w: float(np.mean(v)) for w, v in top5.items()})


def main():
    auc = smell_model_per_word()
    top1, top5 = nose_per_word()
    res = {
        "smell_model_mean_auc": float(np.mean(list(auc.values()))),
        "smell_model_auc_per_word": auc,
        "nose_top1": float(np.mean(list(top1.values()))),
        "nose_top5": float(np.mean(list(top5.values()))),
        "nose_top5_per_word": top5,
        "chance_top1": 1 / 138, "chance_top5": TOP / 138,
    }
    with open(os.path.join(HERE, "evaluation.json"), "w") as f:
        json.dump(res, f, indent=1)

    def show(title, d, n=8):
        s = sorted(d, key=d.get, reverse=True)
        print(f"\n{title}\n  best : " + ", ".join(f"{w} {d[w]:.2f}" for w in s[:n]))
        print("  worst: " + ", ".join(f"{w} {d[w]:.2f}" for w in s[-n:]))

    print(f"Smell model mean ROC-AUC: {res['smell_model_mean_auc']:.3f}")
    show("Smell model per-word ROC-AUC", auc)
    print(f"\nNose, single-word sniffs: top-1 {res['nose_top1']:.1%} "
          f"(chance {res['chance_top1']:.1%}), top-5 {res['nose_top5']:.1%} "
          f"(chance {res['chance_top5']:.1%})")
    show("Nose top-5 hit rate per word", top5)
    for w in ["coffee", "lavender", "fruity", "smoky", "mint", "lemon", "banana", "vanilla"]:
        if w in top5:
            print(f"  {w:10s} top-5 {top5[w]:.0%}  smell-model AUC {auc.get(w, float('nan')):.2f}")


if __name__ == "__main__":
    main()
