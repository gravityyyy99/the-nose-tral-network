"""Understand what smell the user typed, fixing spelling mistakes.

Vocabulary = the 138 smell words of the dataset + the six curated samples.
"""
import difflib
import re

import sensor
import smell_model

AUTOCORRECT_CUTOFF = 0.75   # close enough to silently fix (and tell the user)
SUGGEST_CUTOFF = 0.5        # close enough to offer as a suggestion


def vocabulary():
    words = list(smell_model._load()["labels"])
    return sorted(set(words) | set(sensor.load_samples()))


def resolve_one(token):
    """-> dict(status, word, original, suggestions); status: ok | corrected | unknown"""
    original = token
    token = re.sub(r"\s+", " ", token.strip().lower())
    vocab = vocabulary()
    if token in vocab:
        return {"status": "ok", "word": token, "original": original, "suggestions": []}
    best = difflib.get_close_matches(token, vocab, n=1, cutoff=AUTOCORRECT_CUTOFF)
    if best:
        return {"status": "corrected", "word": best[0], "original": original, "suggestions": []}
    sugg = difflib.get_close_matches(token, vocab, n=5, cutoff=SUGGEST_CUTOFF)
    return {"status": "unknown", "word": None, "original": original, "suggestions": sugg}


def resolve(text):
    """Split 'coffe, fruty and smoky' into tokens and resolve each."""
    tokens = [t for t in re.split(r",|\band\b|\+|;", text) if t.strip()]
    return [resolve_one(t) for t in tokens]


def molecules_for(word, rng, n=6):
    """SMILES that make up this smell: curated sample, or dataset molecules with that label."""
    samples = sensor.load_samples()
    if word in samples:
        return list(samples[word]["molecules"].values())
    pool = smell_model.word_pool(word)
    idx = rng.choice(len(pool), size=min(n, len(pool)), replace=False)
    return [pool[i] for i in idx]
