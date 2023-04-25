#!/usr/bin/env python3

import sys
import os
import re
import numpy
from nltk import pos_tag, Text, tokenize
from nltk.collocations import BigramCollocationFinder
from nltk.corpus import stopwords
from nltk.metrics import BigramAssocMeasures
import spacy
from spacy.lang.en import English
from spacy import tokenizer
from spacy.lang.en.stop_words import STOP_WORDS
from nltk.corpus import words
from collections import Counter

nlp = spacy.load("en_core_web_lg")

def keep_token(tok):
  return tok.pos_ not in {"NUM", "SYM", "PUNC", "SPACE"}

##stuff = "NOUN", "ADJ", "PROPN", "VERB", "ADV", "PRON"

##english_stopwords = set(stopwords.words("english"))
##additional_stopwords = {"esq","arctic","british","zoology","pennant","thomas","author","date","title","indian","oxford","fig","tab","lin" "syst","voy","exped","quad","plate", "plates","syn","hist","buffon","vol","class","div","introduction","advertisement","preface","synopsis"}
##english_stopwords.update(additional_stopwords)

##STOP_WORDS |= {"esq","arctic","british","zoology","pennant","thomas","author","date","title","indian","oxford","fig","tab","lin" "syst","voy","exped","quad","plate", "plates","syn","hist","buffon","vol","class","div","introduction","advertisement","preface","synopsis"}

##roman_numerals = re.search("\w*[MDCLXVI][\.]", re.IGNORECASE | re.MULTILINE)

def get_texts(path_to_files):
    words = []
    for author in os.scandir(path_to_files):
        for file in os.scandir(author.path):
            with open(file.path, encoding="utf-8") as input_file:
                text = input_file.read()
                #text = re.sub(r"\[[^\]]+?\]", "", text)
                text = re.sub(r"\w*[mdclxviMDCLXVI][\.]", "", text)
                text = text.lower()
                doc = nlp(text)
                word_freq = Counter(words)
                common_words = word_freq.most_common(2)
                english_stopwords = set(stopwords.words("english"))
                additional_stopwords = {"quadrupeds", "land","order","birds","esq","arctic","british","zoology","pennant","thomas","author","date","title","indian","oxford","fig","tab","lin" "syst","voy","exped","quad","plate", "plates","syn","hist","buffon","vol","class","div","introduction","advertisement","preface","synopsis"}
                english_stopwords.update(additional_stopwords)
                english_stopwords.update(common_words)
                new_doc = list(filter(keep_token, doc))
            #tokens = [token for token in new_doc if token not in ]
            filtered_tokens = [
                token for token in new_doc if token not in english_stopwords
            ]
            words.extend(filtered_tokens)
    return words

if __name__ == "__main__":
    path = "/Users/claud/texts/zoology/html"
    window_size = int(3)

    print("Get all text...")
    words = get_texts(path)

    print("Building co-occurrence representation...")
    bcf = BigramCollocationFinder.from_words(words, window_size=window_size)

    print("Computing top 10 word associations using log-likelihood...")
    print(bcf.nbest(BigramAssocMeasures.likelihood_ratio, 10))

    print("Computing top 10 word association using PMI...")
    print(bcf.nbest(BigramAssocMeasures.pmi, 10))

    while True:
        word = input("Type a word to get top 5 associated words (CTRL+C to quit): ")
        pmi_scores = []
        likelihood_scores = []
        for target_word in bcf.word_fd:
            pmi_score = bcf.score_ngram(BigramAssocMeasures.pmi, word, target_word)
            likelihood_score = bcf.score_ngram(BigramAssocMeasures.likelihood_ratio, word, target_word)
            if pmi_score:
                pmi_scores.append((target_word, pmi_score))
            if likelihood_score:
                likelihood_scores.append((target_word, likelihood_score))

        for measure, scores in [
            ("Log-likelihood score", likelihood_scores),
            ("Pointwise Mutual Information", pmi_scores),
        ]:
            print(f"\n### Top 5 associated words as measured by {measure} ###")
            for target_word, score in sorted(scores, key=lambda x: x[1], reverse=True)[:5]:
                print(f"{target_word}: {score}")

