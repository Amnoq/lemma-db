# lemma-bank

A multilingual word→lemma mapping bank with corpus frequencies — the
mapping layer of a prediction instrument. 715,769 surface forms across
five languages resolve to their dictionary forms (lemmas), with
honest unknowns: a form with no mapping returns nothing, never a guess.

## Quick start

```bash
python3 build.py        # downloads sources, builds the JSON bank (~1 min)
python3 - <<'EOF'
from lemma_api import LemmaDB
db = LemmaDB()
print(db.lemmatize("running"))            # run
print(db.lemmatize("অঙ্গগুলা", "ben"))     # অঙ্গ
print(db.frequency("run"))                # 44715 (BNC)
print(db.form_frequency("καί", "grc"))    # 1556241 (~25M-token Greek corpus)
print(db.coverage("the running geese".split()))
EOF
```

## What's here

| File | What it is |
|---|---|
| `lemma_api.py` | The lookup API: `lemmatize`, `frequency`, `form_frequency`, `coverage`, `languages` |
| `build.py` | Reproducible build: fetches every upstream source and regenerates the bank |
| `form2lemma.json` | English: 182,903 forms → 84,487 lemmas (generated) |
| `lemma_freq.json` | English: lemma → BNC frequency (generated) |
| `unimorph/*_form2lemma.json` | Bengali / Urdu / Ancient Greek / Latin form→lemma (generated) |
| `greek_freq/` | Ancient Greek form counts, ~25.3M tokens (generated) |
| `linken/` | LinkEn lemma bank parse: PoS tags + written variants (English) |
| `LICENSE` | CC-BY-SA 4.0 (see below) |

Generated data is gitignored — `build.py` is the source of truth.

## Data sources & attribution

| Source | Used for | License |
|---|---|---|
| [skywind3000/lemma.en](https://github.com/skywind3000/lemma.en) — English Lemma Database, BNC-referenced | English forms + frequencies | MIT |
| [UniMorph](https://unimorph.github.io/) `ben`, `urd`, `grc`, `lat` | Bengali / Urdu / Ancient Greek / Latin paradigms | CC-BY-SA 3.0 |
| [open-greek/dilemma](https://github.com/open-greek/dilemma) `hunspell_grc_form_freq` | Ancient Greek form frequencies | MIT |
| [LinkEn](https://github.com/lorenzoaugello/LinkEn) (Augello & Passarotti, LDL-2026) | English lemma PoS / variants | see upstream |

UniMorph citation: Sylak-Glassman, Kirov, Yarowsky & Que (2015),
*A language-independent feature schema for inflectional morphology*,
ACL-IJCNLP.

## Design rules

1. **Exact mappings only.** Statistical stemming is a documented
   fallback for languages with no bank — it never silently fills a gap.
2. **Frequencies are reported, not estimated.** A language with no
   frequency layer returns 0, not a guess.
3. **Collisions keep the first lemma.** 4,451 English forms sit under
   more than one lemma; the bank records the first and documents the rule.

## Known limitations

- Cross-source normalization differs (e.g. the Greek frequency list
  lowercases; UniMorph keeps its own conventions), so layers join only
  where normalizations agree.
- UniMorph Latin's lemma inventory has gaps (common verbs like
  *amare* are absent) — coverage, not completeness.

## License

CC-BY-SA 4.0 (see `LICENSE`) — the share-alike terms of the UniMorph
data flow through to the bank. The Python code is additionally usable
under MIT at the author's discretion.
