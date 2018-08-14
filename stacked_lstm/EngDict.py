import nltk
from nltk.corpus import wordnet

def get_synonyms(word):
    synonyms = []

    for syn in wordnet.synsets(word):

        for l in syn.lemmas():
            if(l.name() != word):
                synonyms.append(l.name())
    synonyms = list(set(synonyms))
    return synonyms

list_a = get_synonyms('areas')
for l in list_a:
    print(l)