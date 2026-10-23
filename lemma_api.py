#!/usr/bin/env python3
"""lemma_api.py — the mapping layer's working prototype.

One lookup across every language in the bank:
  English (182,903 forms -> 84,487 lemmas, BNC frequencies)
  + UniMorph Bengali / Urdu / Ancient Greek form->lemma maps.

Unknown words return None (honest gap) rather than a guessed stem;
the statistical stemmers in ~/workspace/stemmers/ are the documented
fallback for languages with no exact bank.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

LANG_NAMES = {
    "en": "English",
    "ben": "Bengali",
    "urd": "Urdu",
    "grc": "Ancient Greek",
    "lat": "Latin",
}


class LemmaDB:
    def __init__(self):
        self.maps = {}
        self.maps["en"] = json.load(open(os.path.join(HERE, "form2lemma.json"),
                                         encoding="utf-8"))
        self.freq = json.load(open(os.path.join(HERE, "lemma_freq.json"),
                                   encoding="utf-8"))
        for lang in ("ben", "urd", "grc", "lat"):
            p = os.path.join(HERE, "unimorph", f"{lang}_form2lemma.json")
            if os.path.exists(p):
                self.maps[lang] = json.load(open(p, encoding="utf-8"))
        # Ancient Greek form frequencies: open-greek/dilemma
        # hunspell_grc_form_freq.json (~25.3M tokens, 76k forms).
        self.form_freq = {}
        gp = os.path.join(HERE, "greek_freq", "hunspell_grc_form_freq.json")
        if os.path.exists(gp):
            self.form_freq["grc"] = json.load(
                open(gp, encoding="utf-8"))["forms"]

    def languages(self):
        return {k: (LANG_NAMES.get(k, k), len(v))
                for k, v in self.maps.items()}

    def lemmatize(self, word, lang="en"):
        """Exact form->lemma. Returns None when the form is not in the bank."""
        m = self.maps.get(lang)
        if not m:
            return None
        if word in m:
            return m[word]
        low = word.lower()
        if low in m:
            return m[low]
        return None

    def frequency(self, lemma):
        """BNC frequency for English lemmas; 0 when unlisted."""
        return self.freq.get(lemma, 0)

    def form_frequency(self, word, lang="en"):
        """Corpus count for a surface form. Greek: ~25.3M-token
        dilemma ngram counts. Other languages: 0 (no frequency
        layer yet) — reported, not estimated."""
        return self.form_freq.get(lang, {}).get(word, 0)

    def coverage(self, words, lang="en"):
        """Fraction of tokens with an exact mapping. Empirical, not a claim."""
        words = list(words)
        if not words:
            return 0.0
        hit = sum(1 for w in words if self.lemmatize(w, lang) is not None)
        return hit / len(words)


if __name__ == "__main__":
    db = LemmaDB()
    print("languages:", db.languages())
    tests = [
        ("running", "en"), ("geese", "en"), ("better", "en"),
        ("Unknownword", "en"),
    ]
    for w, lang in tests:
        lemma = db.lemmatize(w, lang)
        print(f"{w} -> {lemma}  (freq {db.frequency(lemma) if lemma else '-'})")
    # UniMorph spot checks (forms pulled live from the paradigm tables)
    for lang, forms in {
        "ben": None, "urd": None, "grc": None,
    }.items():
        m = db.maps[lang]
        sample = list(m.items())[:3]
        print(f"{lang} sample:", sample)
    print("en coverage on test sentence:",
          db.coverage("the running geese flew better than before".split()))
