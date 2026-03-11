import re   
from typing import List

import pymorphy3


class Lemmatizer: 

    _WORD_VARIANTS = re.compile(r"[а-яёА-ЯЁa-zA-Z]+", re.UNICODE)

    def __init__(self) -> None:
        self._morph = pymorphy3.MorphAnalyzer()

    def extract_and_lematize(self, text: str) -> List[str]:
        words = self._WORD_VARIANTS.findall(text)

        lemmas = []

        for word in words:
            parsed = self._morph.parse(word.lower())
            if parsed:
                lemma = parsed[0].normal_form
            else:
                lemma = word.lower()
            lemmas.append(lemma)
        
        return lemmas
    
    