#!/usr/bin/env python3
"""build.py — reproducibly build the lemma bank from upstream sources.

Downloads the sources, parses them into the JSON bank, and writes the
files lemma_api.py reads. Generated data is gitignored; this script is
the source of truth.

    python3 build.py

Sources (all fetched live; see README for licenses):
  English ..... skywind3000/lemma.en (lemma.en.txt)
  ben/ur/grc/lat .. UniMorph TSVs (github.com/unimorph/<iso>)
  Greek freq .. open-greek/dilemma (hunspell_grc_form_freq.json.gz)
"""
import gzip
import json
import os
import shutil
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UNIMORPH_LANGS = ["ben", "urd", "grc", "lat"]


def fetch(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    print("fetch", url)
    urllib.request.urlretrieve(url, dest)
    return dest


def build_english():
    src = fetch("https://raw.githubusercontent.com/skywind3000/lemma.en/master/lemma.en.txt",
                os.path.join(HERE, "_dl", "lemma.en.txt"))
    form2lemma, lemma_freq = {}, {}
    collisions = 0
    with open(src, encoding="utf-8") as f:
        for line in f:
            line = line.split(";")[0].strip()  # strip comments
            if not line or "->" not in line:
                continue
            head, forms = line.split("->", 1)
            head = head.strip()
            if "/" in head:
                lemma, freq = head.rsplit("/", 1)
                lemma, freq = lemma.strip(), int(freq.strip() or 0)
            else:
                lemma, freq = head, 0
            lemma_freq[lemma] = freq
            # the lemma maps to itself (a form like any other)
            if lemma not in form2lemma:
                form2lemma[lemma] = lemma
            for form in forms.split(","):
                form = form.strip()
                if not form:
                    continue
                if form in form2lemma:
                    collisions += 1
                    continue  # first lemma wins (documented)
                form2lemma[form] = lemma
    json.dump(form2lemma, open(os.path.join(HERE, "form2lemma.json"), "w", encoding="utf-8"),
              ensure_ascii=False, separators=(",", ":"))
    json.dump(lemma_freq, open(os.path.join(HERE, "lemma_freq.json"), "w", encoding="utf-8"),
              ensure_ascii=False, separators=(",", ":"))
    print(f"en: {len(form2lemma)} forms, {len(lemma_freq)} lemmas, {collisions} collisions")


def build_unimorph(lang):
    src = fetch(f"https://raw.githubusercontent.com/unimorph/{lang}/master/{lang}",
                os.path.join(HERE, "_dl", f"{lang}.tsv"))
    f2l, collisions, n = {}, 0, 0
    with open(src, encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 2:
                continue
            lemma, form = parts[0].strip(), parts[1].strip()
            n += 1
            if form in f2l:
                collisions += 1
                continue  # first lemma wins (documented)
            f2l[form] = lemma
    out = os.path.join(HERE, "unimorph", f"{lang}_form2lemma.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(f2l, open(out, "w", encoding="utf-8"),
              ensure_ascii=False, separators=(",", ":"))
    print(f"{lang}: {len(f2l)} forms from {n} rows, {collisions} collisions")


def build_greek_freq():
    gz = fetch("https://raw.githubusercontent.com/open-greek/dilemma/main/data/hunspell_grc_form_freq.json.gz",
               os.path.join(HERE, "_dl", "hunspell_grc_form_freq.json.gz"))
    out = os.path.join(HERE, "greek_freq", "hunspell_grc_form_freq.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with gzip.open(gz, "rt", encoding="utf-8") as fin, \
            open(out, "w", encoding="utf-8") as fout:
        shutil.copyfileobj(fin, fout)
    d = json.load(open(out, encoding="utf-8"))
    print(f"grc freq: {len(d['forms'])} forms")


def main():
    build_english()
    for lang in UNIMORPH_LANGS:
        build_unimorph(lang)
    build_greek_freq()
    print("done. generated data is gitignored; see README.")


if __name__ == "__main__":
    main()
