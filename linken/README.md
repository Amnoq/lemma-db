# LinkEn lemma bank (parsed 2026-10-08)

Source: lorenzoaugello/LinkEn `ttl/lemmabank_linken.ttl` (4.38 MB Turtle RDF),
from "Towards the LinkEn Knowledge Base" (LDL-2026). CC BY-NC 4.0 proceedings;
repo data as published.

Built with a hybrid neuro-symbolic pipeline (Gemini 2.5 Flash generating RDF
under OntoLex-Lemon/LiLa ontology constraints + human correction loop).
Notably, one of its input lemma sources was skywind3000/lemma.en — the same
list behind `../form2lemma.json`.

- `lemmabank_linken.ttl` — source RDF (21,276 lemmas + 3,463 hypolemmas)
- `lemma_pos.json` — label -> [PoS...] (UPOS-aligned: noun, verb, adjective,
  adverb, ...); 20,131 labels, 4,404 multi-PoS (e.g. run -> noun+verb)
- `lemma_written_variants.json` — label -> extra orthographic variants
  (547 labels, e.g. centre -> center)
- `hypolemma_of.json` — hypolemma -> base lemma (deadjectival adverbs and
  adjectival participles, e.g. slowly->slow, broken->break)

Caveat (paper's own evaluation): PoS accuracy ~99% on single-PoS lemmas, but
the LLM over-generated on multi-PoS words (precision dip) — treat multi-PoS
tags as candidate, not gold.
