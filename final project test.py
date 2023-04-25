
import os
import re
import sys
import nltk
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import numpy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

Arctic_Zoology_Sample = "THE Sheep, in its wild state, inhabits the north-east of Asia, beyond lake Baikal, between the Onon and Argun, to the height of latitude 60, on the east of the Lena, and from thence to Kamtschatka, and perhaps the Kurili islands. I dare not pronounce that they extend to the continent of America; yet I have received from Doctor Pallas a fringe of very fine twisted wool, which had or­namented a dress from the isle of Kadjak; and I have myself another piece from the habit of the Americans in latitude 50. The first was of a snowy whiteness, and of unparalleled fineness; the other as fine, but of a pale brown color: the first appeared to be the wool which grows intermixed with the hairs of the Argali; the last, that which is found beneath those of the Musk Ox. Each of these animals may exist on that side of the continent, notwithstanding they might have not fallen within the reach of the navigators in their short stay off the coast. Certain quadrupeds of this genus were observed in California by the missionaries in 1697; one as large as a Calf of one or two years old, with a head like a Stag, and horns like a Ram: the tail and hair speckled, and shorter than a Stag's. A second kind was larger, and varied in color; some being white, others black, and furnished with very good wool. The Fathers called both Sheep, from their great resemblance to them*. Either the Americans of latitude 50 are pos­sessed of these animals, or may obtain the fleeces by commerce from the southern Indians. The Argali abound in Kamtschatka; they are the most useful of their animals, for they contribute to food and cloathing. The Kamtschatkans cloath themselves with the skins, and esteem the flesh, especially the fat, diet fit for the Gods. There is no labor which they will not undergo in the chase. They abandon their habitations, with all their family, in the spring, and continue the whole summer in the employ, amidst the rude mountains, fearless of the dreadful precipices, or of the avelenches, which often overwhelm the eager sportsmen. These animals are shot with guns or with arrows; sometimes with cross-bows, which are placed in the paths, and discharged by means of a string whenever the Argali happens to tread on it. They are often chased with dogs, not that they are overtaken by them; but when they are driven to the lofty summits, they will often stand and look as if it were with contempt on the dogs below, which gives the hunter an opportunity of creeping within reach while they are so engaged; for they are the shyest of animals. The Mongols and Tungusi use a nobler species of chase:They collect together a vast multitude of horses and dogs, attempting to sur­round them on a sudden; for such is their swiftness and cunning, that if they perceive, either by sight or smell, the approach of the chasseurs, they instantly take to flight, and secure themselves on the lofty and inaccessible summits. Domesticated Sheep will live even in the dreadful climate of Greenland. Mr. Fabricius"

def get_files(path_to_files):
    docs = []
    english_stopwords = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    for file in os.scandir(path_to_files):
        with open(file.path) as input_file:
            text = input_file.read()
            text = re.sub(r"<[^>]+>", "", text)
        tokens = re.findall("\w+", text)
        filtered_tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in english_stopwords]
        docs.append((file.name, " ".join(filtered_tokens)))
    return docs

with open("Indian_Zoology.txt") as text_file:
    file_name=text_file.read()

#Arctic_Zoology_Vol_1_text = open(file_name, encoding="utf8").read()
#Arctic_Zoology_Vol_1_doc = nlp(Arctic_Zoology_Vol_1_text)
#print ([token.text for token in Arctic_Zoology_Vol_1_text])

