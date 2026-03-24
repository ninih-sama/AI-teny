import re


class MalagasyLemmatizer:
    def __init__(self):
        # Liste simplifiée des préfixes malgaches
        self.prefixes = ["man", "mamp", "mana", "mi", "maha", "ma", "m"]
        # Liste simplifiée des suffixes
        self.suffixes = ["ina", "ana", "ena"]

    def lemmatize(self, word):
        word = word.lower().strip()
        # On retire les préfixes
        for p in self.prefixes:
            if word.startswith(p) and len(word) > len(p) + 2:
                word = word[len(p) :]
                break
        # On retire les suffixes
        for s in self.suffixes:
            if word.endswith(s) and len(word) > len(s) + 2:
                word = word[: -len(s)]
                break
        return word
