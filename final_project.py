#!/usr/bin/env python3

import sys
import os
import re
import numpy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, Text, tokenize
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures


def get_files(path_to_files):
    words = []
    nouns = []
    adj = []
    english_stopwords = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    for author in os.scandir(path_to_files):
        for file in os.scandir(author.path):
            with open(file.path, encoding="utf-8") as input_file:
                text = input_file.read()
                text = re.sub(r"<[^>]+>", "", text)
            tokens = re.findall(r"\w+", text)
            text_object = Text(tokens)
            filtered_tokens = [
                lemmatizer.lemmatize(token).lower() for token in tokens if token not in english_stopwords
            ]
            filtered_tokens2 = [w for w in filtered_tokens if not re.search(r'\d', w)]
            text_with_pos = pos_tag(text_object, tagset="universal")
            words.extend(filtered_tokens2)
            noun_words = [word for word, pos in text_with_pos if pos == "NOUN"]
            adj_words = [word for word, pos in text_with_pos if pos == "ADJ"]
            nouns.extend(noun_words)
            adj.extend(adj_words)
    return words, nouns, adj



if __name__ == "__main__":
    path = "/Users/claud/texts/zoology/html"
    window_size = int(2)

    print("Get all text...")
    words, nouns, adj = get_files(path)

    print("Building co-occurrence representation...")
    bcf = BigramCollocationFinder.from_words(words, window_size=window_size)

    print("Computing top 10 word associations using log-likelihood...")
    print(bcf.nbest(BigramAssocMeasures.likelihood_ratio, 10))

    print("Computing top 10 word association using PMI...")
    print(bcf.nbest(BigramAssocMeasures.pmi, 10))

    while True:
        word = input("Type an animal to get top 15 associated words (CTRL+C to quit): ")
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
            print(f"\n### Top 15 associated words as measured by {measure} ###")
            for target_word, score in sorted(scores, key=lambda x: x[1], reverse=True)[:15]:
                print(f"{target_word}: {score}")
