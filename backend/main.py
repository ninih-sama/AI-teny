import os
import json
import re
import collections
import pandas as pd
import jellyfish
import uvicorn
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIGURATION ---
SCRAPED_FILE = "scraped_words.json"
MODEL_FILE = "ngram_model.json"
DICT_FOLDER = "malagasy_dict"
CORPUS_FOLDER = "corpus"


# --- UTILITAIRES ---
def match_case(original, suggestion):
    if original.isupper():
        return suggestion.upper()
    if original[0].isupper():
        return suggestion.capitalize()
    return suggestion.lower()


# --- IA DE CONTEXTE (N-GRAMS) ---
class MalagasyLanguageModel:
    def __init__(self):
        self.bigrams = collections.defaultdict(lambda: collections.defaultdict(int))

    def train(self, text):
        words = re.findall(r"\b[a-zàâéèêëîïôûù]{2,}\b", text.lower())
        for i in range(len(words) - 1):
            self.bigrams[words[i]][words[i + 1]] += 1

    def predict_next(self, last_word):
        if last_word in self.bigrams:
            sorted_next = sorted(
                self.bigrams[last_word].items(), key=lambda x: x[1], reverse=True
            )
            return [word for word, freq in sorted_next[:5]]
        return []

    def save(self):
        with open(MODEL_FILE, "w", encoding="utf-8") as f:
            json.dump(self.bigrams, f, ensure_ascii=False)

    def load(self):
        if os.path.exists(MODEL_FILE):
            with open(MODEL_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for k, v in data.items():
                    self.bigrams[k].update(v)


# --- MOTEUR LINGUISTIQUE ---
class MalagasyGrammarEngine:
    def __init__(self, dictionary_keys):
        self.dict_keys = set(dictionary_keys)
        self.prefixes = [
            "mampifamp",
            "mamp",
            "maha",
            "manka",
            "mifamp",
            "mifan",
            "faha",
            "tafa",
            "voa",
            "man",
            "mi",
            "ma",
            "na",
            "ha",
            "ho",
            "no",
            "i",
            "a",
        ]
        self.suffixes = ["ana", "ina", "na", "ny", "ko", "ao", "tsika", "nay", "areo"]
        self.terminales = ["ka", "tra", "na"]

    def apply_rules(self, word):
        w = word.lower().strip()
        if w in self.dict_keys:
            return w, "exact"
        if "-" in w:
            base = w.split("-")[0]
            if any(f"{base}{t}" in self.dict_keys for t in self.terminales):
                return w, "combinaison"
        for s in sorted(self.suffixes, key=len, reverse=True):
            if w.endswith(s):
                stem = w[: -len(s)]
                if stem in self.dict_keys:
                    return stem, "suffix"
        for p in sorted(self.prefixes, key=len, reverse=True):
            if w.startswith(p):
                root = w[len(p) :]
                if root in self.dict_keys:
                    return root, "prefix"
        return None, "unknown"


# --- CHARGEMENT ---
def load_all_data():
    all_defs = {}
    if os.path.exists(DICT_FOLDER):
        for f in os.listdir(DICT_FOLDER):
            if f.endswith(".csv"):
                try:
                    df = pd.read_csv(
                        os.path.join(DICT_FOLDER, f),
                        sep=None,
                        engine="python",
                        encoding="utf-8",
                    )
                    all_defs.update(
                        dict(zip(df.iloc[:, 0].astype(str).str.lower(), df.iloc[:, 1]))
                    )
                except:
                    pass
    if os.path.exists(SCRAPED_FILE):
        with open(SCRAPED_FILE, "r", encoding="utf-8") as f:
            all_defs.update(json.load(f))
    return all_defs


DEFINITIONS = load_all_data()
DICTIONNAIRE_POUR_CORRECTION = list(DEFINITIONS.keys())
GRAMMAR = MalagasyGrammarEngine(DEFINITIONS.keys())
IA_MODEL = MalagasyLanguageModel()
IA_MODEL.load()


class TextRequest(BaseModel):
    text: str


# --- ENDPOINT ANALYZE (VERSION CIBLÉE AVEC PROTECTION LISTES) ---
@app.post("/analyze")
async def analyze(data: TextRequest):
    tokens = re.findall(r"[\wàâéèêëîïôûù\-]+|[^\wàâéèêëîïôûù\-]+", data.text)
    results = []
    corrections_list = []
    has_error = False

    for token in tokens:
        # 1. PROTECTION : Si ce n'est pas un mot (espaces, sauts de ligne, symboles)
        if not re.search(r"[\wàâéèêëîïôûù]", token):
            results.append(
                {"original": token, "suggestion": "", "status": "punctuation"}
            )
            continue

        # 2. PROTECTION : Ne pas corriger les numérotations (ex: "1.", "12.", "1")
        # Cette RegEx détecte les chiffres seuls ou suivis d'un point
        if re.match(r"^\d+\.?$", token):
            results.append({"original": token, "suggestion": "", "status": "correct"})
            continue

        clean_w = token.lower()
        root, rule = GRAMMAR.apply_rules(clean_w)

        if root or clean_w in DICTIONNAIRE_POUR_CORRECTION:
            status, suggestion, definition = "correct", "", ""
        else:
            if not DICTIONNAIRE_POUR_CORRECTION:
                status, suggestion, definition = "correct", "", ""
            else:
                best_match = min(
                    DICTIONNAIRE_POUR_CORRECTION,
                    key=lambda x: jellyfish.levenshtein_distance(clean_w, x),
                )
                dist = jellyfish.levenshtein_distance(clean_w, best_match)
                limit = 1 if len(clean_w) <= 4 else 2

                if dist <= limit:
                    status = "error"
                    suggestion = match_case(token, best_match)
                    definition = DEFINITIONS.get(best_match, "Tsy hita")
                    has_error = True
                    corrections_list.append(
                        {
                            "original": token,
                            "suggestion": suggestion,
                            "definition": definition,
                        }
                    )
                else:
                    status, suggestion, definition = "correct", "", ""

        results.append({"original": token, "suggestion": suggestion, "status": status})

    if not has_error:
        return {"full_correction": "", "corrections_only": [], "status": "clean"}

    full_text = "".join(
        [r["suggestion"] if r["status"] == "error" else r["original"] for r in results]
    )

    return {
        "full_correction": full_text,
        "corrections_only": corrections_list,
        "status": "modified",
    }


# --- STARTUP ---
@app.on_event("startup")
async def startup_event():
    if not os.path.exists(CORPUS_FOLDER):
        os.makedirs(CORPUS_FOLDER)
    for filename in os.listdir(CORPUS_FOLDER):
        if filename.endswith(".txt"):
            with open(
                os.path.join(CORPUS_FOLDER, filename), "r", encoding="utf-8"
            ) as f:
                content = f.read().lower()
                IA_MODEL.train(content)
                for w in set(re.findall(r"\b[a-zàâéèêëîïôûù\-]{3,}\b", content)):
                    if w not in DEFINITIONS:
                        DEFINITIONS[w] = f"Auto-validé : {filename}"
    global DICTIONNAIRE_POUR_CORRECTION
    DICTIONNAIRE_POUR_CORRECTION = list(DEFINITIONS.keys())
    GRAMMAR.dict_keys = set(DICTIONNAIRE_POUR_CORRECTION)
    IA_MODEL.save()
    with open(SCRAPED_FILE, "w", encoding="utf-8") as f:
        json.dump(DEFINITIONS, f, ensure_ascii=False)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
