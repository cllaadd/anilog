#!/usr/bin/env python3
import spacy
import sys
import os
import re
from spacy.lang.en import English
#from spacy.pipeline import tagger
#from spacy.pipeline import ner
from spacy import tokenizer
from spacy import displacy
from spacy.lang.en.stop_words import STOP_WORDS
import numpy
import srsly
import textacy
from textacy import preprocessing
from gensim.models import word2vec
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss



nlp = spacy.load("en_core_web_lg")




def find_indices(text):
  title, filename = text
  with open(filename) as input_file:
    full_text = input_file.readlines()
    index_start = 0
    index_end = 100
    if title == "AZ1":
      for line_number, line in enumerate(full_text):
          index_start = line_number + 6
          index_end = line_number + 49
          break
    elif title == "AZ2":
      for line_number, line in enumerate(full_text):
          index_start = line_number + 6
          index_end = line_number + 416
          break
    elif title == "IZ":
      for line_number, line in enumerate(full_text):
          index_start = line_number + 11
          index_end = line_number - 13
          break
    index_only = full_text[index_start:index_end]
    index = [i[2:] for i in index_only]
    indicies = []
    for title, file in text:
      indicies.append(title, index) 
    return indicies

if __name__ == "__main__":
  documents = [
        ("AZ1", "/Users/claud/texts/zoology/html/AZ1.txt"),
        ("AZ2", "/Users/claud/texts/zoology/html/AZ2.txt"),
        ("IZ", "/Users/claud/texts/zoology/html/IZ.txt"),
    ]
  all_sections = []
  for doc in documents:
    sections = find_indices(doc)
    all_sections.extend(sections)
  print(sections)
 



with open("/Users/claud/texts/zoology/html/IZ.txt", "r") as input_file:
    full_text = input_file.read().splitlines()
    index_start = 11
    index_end = 87
    index_only = full_text[index_start:index_end]
    indexIZ = [i[2:] for i in index_only]





def stop_token(tok):
  for token in doc:
    if token.is_stop == False:
      return token


def keep_token(tok):
  return tok.pos_ not in {'PUNCT', 'NUM', 'SYM'}

#final_tokens = list(filter(keep_token, doc))

#filtered_tokens = [token.text for token in doc if not token.is_stop] 



Arctic_Zoology_Sample = "THE Sheep, in its wild state, inhabits the north-east of Asia, beyond lake Baikal, [Page v] between the Onon and Argun, to the height of latitude 60, on the east of the Lena, and from thence to Kamtschatka, and perhaps the Kurili islands. I dare not pronounce that they extend to the continent of America; yet I have received from Doctor Pallas a fringe of very fine twisted wool, which had or­namented a dress from the isle of Kadjak; and I have myself another piece from the habit of the Americans in latitude 50. The first was of a snowy whiteness, and of unparalleled fineness; the other as fine, but of a pale brown color: the first appeared to be the wool which grows intermixed with the hairs of the Argali; the last, that which is found beneath those of the Musk Ox. Each of these animals may exist on that side of the continent, notwithstanding they might have not fallen within the reach of the navigators in their short stay off the coast. Certain quadrupeds of this genus were observed in California by the missionaries in 1697; one as large as a Calf of one or two years old, with a head like a Stag, and horns like a Ram: the tail and hair speckled, and shorter than a Stag's. A second kind was larger, and varied in color; some being white, others black, and furnished with very good wool. The Fathers called both Sheep, from their great resemblance to them*. Either the Americans of latitude 50 are pos­sessed of these animals, or may obtain the fleeces by commerce from the southern Indians. The Argali abound in Kamtschatka; they are the most useful of their animals, for they contribute to food and cloathing. The Kamtschatkans cloath themselves with the skins, and esteem the flesh, especially the fat, diet fit for the Gods. There is no labor which they will not undergo in the chase. They abandon their habitations, with all their family, in the spring, and continue the whole summer in the employ, amidst the rude mountains, fearless of the dreadful precipices, or of the avelenches, which often overwhelm the eager sportsmen. These animals are shot with guns or with arrows; sometimes with cross-bows, which are placed in the paths, and discharged by means of a string whenever the Argali happens to tread on it. They are often chased with dogs, not that they are overtaken by them; but when they are driven to the lofty summits, they will often stand and look as if it were with contempt on the dogs below, which gives the hunter an opportunity of creeping within reach while they are so engaged; for they are the shyest of animals. The Mongols and Tungusi use a nobler species of chase:They collect together a vast multitude of horses and dogs, attempting to sur­round them on a sudden; for such is their swiftness and cunning, that if they perceive, either by sight or smell, the approach of the chasseurs, they instantly take to flight, and secure themselves on the lofty and inaccessible summits. Domesticated Sheep will live even in the dreadful climate of Greenland. Mr. Fabricius"

test = open("/Users/claud/texts\zoology/html/bp.txt", encoding="utf8").read()


#nlp.add_pipe(nlp.create_pipe('sectionizer')) # updated
doc = nlp(test)
#sections = [sent.string.strip() for sent in doc.sents]
#print(sections)c
#tagger = nlp.add_pipe("tagger")
#processed = tagger(doc)

#for chunk in doc.noun_chunks:
    #print(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text)

adj_list = [token.text for token in doc if token.pos_ =="ADJ"]
ent_list = [ent.text for ent in doc]
amod_list = [token.text for token in doc if token.dep_ == "amod"]

for token in doc:
  if token.dep_ == "amod":
    amodhead = [token.text, token.head.text]

noun_adj_pairs = {}
for chunk in doc.noun_chunks:
  adj = []
  noun = ""
  for tok in chunk:
    if tok.pos_ == "NOUN":
      noun = tok.text
    if tok.pos_ == "ADJ":
            adj.append(tok.text)
  if adj:
        noun_adj_pairs.update({noun:adj})

print(noun_adj_pairs)


