import pymongo, os
import glob, shutil
import nltk
from nltk import FreqDist
from nltk.util import ngrams
from nltk import word_tokenize
from nltk.collocations import BigramCollocationFinder
from nltk.probability import FreqDist
from nltk.collocations import ngrams
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import stopwords
from collections import Counter
import pickle
import os, glob
from nltk.corpus import wordnet
import inflect, math
from multiprocessing import Pool

db_url = 'mongodb://' + "localhost:27017/local"
client = pymongo.MongoClient(db_url)
db = client['local']
collection = db.get_collection('content_ngrams')
global index, total_len
index = 0
total_len = 0
def update_db(k):
    print(k)
    collection.update({
        'first': k[0],
        'second': k[1],
        'third': k[2],
    }, {
        # '$set':
        #     {'first': k[0],
        #      'second': k[1],
        #      'third': k[1],
        #      'count':fdist[k]
        #      },
        '$inc':
            {
                'count': fdist[k]
            }
    }, True, False)

def gen_ngram(text):
    print('tokenizing')
    tok = nltk.word_tokenize(text)
    print('trigrams')
    trigrams = ngrams(tok, 3)
    print('convert to list')
    A = list(trigrams)
    print('convert to hash')
    global fdist
    fdist = FreqDist(A)

    with open('fdist.pickle', 'wb') as f:
        pickle.dump(fdist, f)

    print('add to db')
    total_len = len(fdist)
    p = Pool(4)
    p.map(update_db, [k for k in fdist])






os.chdir("/Users/wonjun/PycharmProjects/EngDict/data/sentences/abstract/next_data")

complete = {}

try:
    with open('/Users/wonjun/PycharmProjects/EngDict/data/sentences/abstract/next_data/complete_db_2.txt', 'r') as f:
        complete_list = f.read().split('\n')
        complete = {i.split(' ')[0] : 0 for i in complete_list}
except FileNotFoundError as e:
    complete = {}


i = 0

text = ""
for file in glob.glob("*.txt"):
    if not complete.__contains__(file):
        text += open(file, encoding='utf-8').read().lower()
gen_ngram(text)