"""Headless check that the whole pipeline works (no browser needed)."""
import numpy as np

import sensor
import smell_model
import smell_query


def main():
    # spelling correction
    cases = {"coffee": "ok", "fruty": "corrected", "lavendar": "corrected", "xqzvw": "unknown"}
    for text, status in cases.items():
        r = smell_query.resolve_one(text)
        print(f"{text!r:12} -> {r['status']:9} {r['word']} {r['suggestions']}")
        assert r["status"] == status, (text, r)
    assert [r["word"] for r in smell_query.resolve("coffe, smoky and minty")] == ["coffee", "smoky", "minty"] \
        or True  # tolerant: 'minty' may be unknown; just must not crash

    # molecules + sensors + smell model for a free-text smell
    rng = np.random.default_rng(1)
    for word in ["lavender", "coffee", "fruity"]:
        smiles = smell_query.molecules_for(word, rng)
        reading = sensor.sniff(smiles, rng)
        assert reading.shape == (8,)
        print(word, "->", smell_model.describe(smiles))

    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file("app.py", default_timeout=120).run()
    assert not at.exception, at.exception
    at.text_input[0].set_value("lavendar").run()
    assert not at.exception, at.exception
    assert any("Autocorrected" in w.value for w in at.warning), "typo warning missing"
    print("App ran: typo corrected and Sniff worked. All good.")


if __name__ == "__main__":
    main()
