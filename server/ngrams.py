from __future__ import print_function
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
import math
from gensim.models import Word2Vec

from keras.callbacks import LambdaCallback
from keras.layers.recurrent import LSTM
from keras.layers.embeddings import Embedding
from keras.layers import Dense, Activation
from keras.models import Sequential, load_model
from keras.utils.data_utils import get_file
import sys
import numpy as np
import string
import gensim
import chardet
import pymysql.cursors
conn = pymysql.connect(
                       host='localhost',
                       user='strutive07',
                       password='lucys2&&Ekfrlo',
                       db='ngrams',
                       charset='utf8'
                       )
import pymongo
mongo_conn = pymongo.MongoClient('mongodb://root:sniperzkzl@localhost:27017')
db = mongo_conn.thesaurus

class SmallerThenTrigram(Exception):
    pass


def get_ngram(tok, n):
    print("get_ngram()", n)
    filename = str(n) + "grams" + ".pickle"
    #     print("tokenizing")
    #     tok = nltk.word_tokenize(text)
    trigrams = ngrams(tok, n)
    print("freqeuncy cal")
    A = list(trigrams)
    fdist = FreqDist(A)
    print("pickle save")
    with open(filename, 'wb') as f:
        pickle.dump(fdist, f, pickle.HIGHEST_PROTOCOL)

    data = fdist.most_common(50)
    return fdist, A


def get_ngrams_saved(n):
    filename = str(n) + "grams" + ".pickle"
    with open(filename, 'rb') as f:
        fdist = pickle.load(f)
    return fdist


def create_ngram_dict(flist, n, minv=50):
    afdict = {}
    for l in flist:
        if (l[1] < minv):
            break
        for i in range(0, n):
            if l[0][i] in afdict:
                afdict[l[0][i]].append(l)
            else:
                tmp_list = []
                tmp_list.append(l)
                afdict[l[0][i]] = tmp_list
    return afdict


def trigram_to_bigram_LR(tri):
    toRightDict = {};
    toLeftDict = {};
    for l in tri:
        leftTok = (l[0][0], l[0][1])
        rightTok = (l[0][1], l[0][2])
        if leftTok in toRightDict:
            toRightDict[leftTok].append(l)
        else:
            tmp_list = [l]
            toRightDict[leftTok] = tmp_list

        if rightTok in toLeftDict:
            toLeftDict[rightTok].append(l)
        else:
            tmp_list = [l]
            toLeftDict[rightTok] = tmp_list
    return toRightDict, toLeftDict


def ngram_to_bigram_LR(n, ngram):
    if n < 3:
        raise SmallerThenTrigram()
    toRightDict = {}
    toLeftDict = {}
    for l in ngram:
        leftTok = (l[0][0], l[0][1])
        rightTok = (l[0][n - 2], l[0][n - 1])
        if leftTok in toRightDict:
            toRightDict[leftTok].append(l)
        else:
            tmp_list = [l]
            toRightDict[leftTok] = tmp_list

        if rightTok in toLeftDict:
            toLeftDict[rightTok].append(l)
        else:
            tmp_list = [l]
            toLeftDict[rightTok] = tmp_list
    return toRightDict, toLeftDict


def ngram_to_trigram_LR(n, ngram):
    if n < 4:
        raise SmallerThenTrigram()
    toRightDict = {}
    toLeftDict = {}
    for l in ngram:
        leftTok = (l[0][0], l[0][1], l[0][2])
        rightTok = (l[0][n - 3], l[0][n - 2], l[0][n - 1])
        if leftTok in toRightDict:
            toRightDict[leftTok].append(l)
        else:
            tmp_list = [l]
            toRightDict[leftTok] = tmp_list

        if rightTok in toLeftDict:
            toLeftDict[rightTok].append(l)
        else:
            tmp_list = [l]
            toLeftDict[rightTok] = tmp_list
    return toRightDict, toLeftDict


def fivegrams_middle_predict(n, ngram):
    if n < 5:
        raise SmallerThenTrigram()
    toRightDict = {}
    for l in ngram:
        leftTok = (l[0][0], l[0][1], l[0][3], l[0][4])
        if leftTok in toRightDict:
            toRightDict[leftTok].append(l)
        else:
            tmp_list = [l]
            toRightDict[leftTok] = tmp_list
    return toRightDict


def get_synonyms(word):
    synonyms = []

    for syn in wordnet.synsets(word):

        for l in syn.lemmas():
            if (l.name() != word):
                synonyms.append(l.name())
    synonyms = list(set(synonyms))
    return synonyms


def get_name(synset):
    if (type(synset) != int):
        return {'word': synset.name().partition('.')[0], 'type': synset.name().partition('.')[2][0]}
    return {'word': "None", type: "NotWord"}


def get_max_wup_similarity(src, target):
    max_value = 0
    max_el = -1
    #     print(src, target)
    for s in wordnet.synsets(src):
        for t in wordnet.synsets(target):
            try:
                if (s == t):
                    #                     print("con")
                    continue
                #                 print(s, t)

                similarity = s.path_similarity(t)
                #                 print('similarity',similarity)
                # print(max_value, similarity)
                if (max_value < similarity):
                    max_value = similarity
                    max_el = (s, t)
            except:
                continue
    if (max_el == -1):
        return -1, -1, -1
    else:
        return max_el[0], max_el[1], max_value


def chunk2word(word):
    word = word[2:-1]
    data = word.split('-')
    return_word = ""
    for w in data:
        return_word += " " + w
    #     print(return_word)
    return return_word.strip()


def get_similarity_by_chunked_data(src, target):
    collection = db.thesaurus_33
    if (target[0] == '<'):
        target = chunk2word(target)
        # print(target)
        mtarget = collection.find_one({"word": target})
        try:
            mtarget = mtarget['synonyms']
        except Exception as e:
            return -1, -1, -1
        max_value = -1
        max_target = -1
        max_src = -1
        for mt in mtarget:
            for t in mt:
                ssrc, starget, svalue = get_max_wup_similarity(src, t)
                if (svalue == -1): continue
                if (svalue > max_value):
                    max_src = ssrc
                    max_target = starget
                    max_value = svalue
        return max_src, max_target, max_value
    else:
        return get_max_wup_similarity(src, target)


def prediction(word_tuple, param_target, mode=0):
    # mode = 0 -> Right Prediction
    # mode = 1 -> Left Prediction
    max_src = 0
    max_target = 0
    max_value = 0
    pred = []
    if (param_target[0] == '<'):
        param_target = chunk2word(param_target)
    # print(param_target)

    if (mode == 0):
        try:
            with conn.cursor() as cursor:
                sql = """SELECT * from v2_content_trigrams WHERE first=%s AND second=%s ORDER BY count DESC LIMIT 50"""
                cursor.execute(sql, word_tuple)
                rows = cursor.fetchall()
                for i, row in enumerate(rows):
                    # print(row)
                    if (row[4] <= 1):
                        break
                    space_probability = row[4]

                    src, target, value = get_similarity_by_chunked_data(param_target, row[3])
                    if (value == -1):
                        score = math.log(space_probability)
                        score = score * math.log(i + 1)
                        pred.append({"src": param_target, "target": row[3], "value": score})
                    else:
                        score = value * 100 * math.log(space_probability)
                        pred.append({"src": get_name(src), "target": get_name(target), "value": score})

        #                     print({"src": get_name(src), "target": get_name(target), "value": score})

        except Exception as e:
            _, _, tb = sys.exc_info()  # tb -> traceback object
            print('file name = ', __file__)
            print('error line No = {}'.format(tb.tb_lineno))
            print(['error'], e)
    if (len(pred) == 0): return pred
    return sorted(pred, key=lambda x: -x['value'])[:5]

def prediction_by_word2vec(word):
    pred = []
    try:
        for similar, dist in word_model.most_similar(word)[:8]:
            pred.append({"word":similar, "value": dist})
    except Exception as e :
        return []
    return pred
def word2idx(word):
  try:
    return word_model.wv.vocab[word].index
  except Exception as e:
    return 'ERROR'


def idx2word(idx):
  try:
    return word_model.wv.index2word[idx]
  except Exception as e:
    return 'ERROR'

def sample2(preds, temperature=1.0, num_generated = 1):
  if temperature <= 0:
    return np.argmax(preds)
  preds = np.asarray(preds).astype('float64')
  preds = np.log(preds) / temperature
  exp_preds = np.exp(preds)
  preds = exp_preds / np.sum(exp_preds)
  probas = np.random.multinomial(num_generated, preds, 1)
  return probas


def sample2(preds, temperature=1.0, num_generated=1):
    if temperature <= 0:
        return np.argmax(preds)
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(num_generated, preds, 1)
    return probas


def predict_next_lstm(text, num_generated=1):
    word_idxs = []
    print(text)
    for word in nltk.word_tokenize(text):
        tmp_word_idx = word2idx(word)
        if tmp_word_idx == 'ERROR':
            return 'ERROR'
        word_idxs.append(tmp_word_idx)
    print(word_idxs)
    prediction = lstm_model.predict(x=np.array(word_idxs))
    print(prediction)
    probas = sample2(prediction[-1], 0.7, num_generated)

    ind = np.argpartition(probas, -num_generated)[-num_generated:]
    # plot_model(model, to_file='model.png')rated:]
    #     print(probas.shape)
    i = 0
    res = []
    for l in probas[0]:
        if (l != 0):
            res.append(idx2word(i))
        i += 1
    return res

def main(isSaved=True):
    
    print('get corpus data')
    global data
    data = ""
    # for file in glob.glob("*.txt"):
    #     data += open(file, encoding='utf-8').read().lower()
    # tmp_sentences = data.split('\n')
    # global sentences
    # print('tokenizing')
    # sentences = [[word for word in nltk.word_tokenize(sentence_one)] for sentence_one in tmp_sentences]
    # print('line cnt', len(sentences))
    global tri_fdist
    global bi_fdist
    global four_fdist, five_fdist
    global toRight_tri2bi, toLeft_tri2bi, toRight_four2bi, toLeft_four2bi, toRight_five2bi, toLeft_five2bi
    global toRight_four2tri, toLeft_four2tri, toRight_five2tri, toLeft_five2tri
    global fivegrams_middle
    global word_model, lstm_model
    if isSaved == True:
        print('saved mode')
        print('get ngrams data')
#        tri_fdist = get_ngrams_saved(3)
        #bi_fdist = get_ngrams_saved(2)
        # four_fdist = get_ngrams_saved(4)
        # five_fdist = get_ngrams_saved(5)
#        print('get ngram dict data')
#        with open('toRight_tri2bi.bin', 'rb') as f:
#            toRight_tri2bi = pickle.load(f)
#        with open('toLeft_tri2bi.bin', 'rb') as f:
#            toLeft_tri2bi = pickle.load(f)

        word_model = Word2Vec.load('../data/word2vecData.model')
        pretrained_weights = word_model.wv.syn0
        vocab_size, emdedding_size = pretrained_weights.shape
        print('Result embedding shape:', pretrained_weights.shape)
        lstm_model = load_model('../data/word2vec_lstm_gen.model')
        print('prediction', predict_next_lstm('weight can only', 1))
        # with open('fivegrams_middle.bin', 'rb') as f:
        #     fivegrams_middle = pickle.load(f)
    # else:
    #     print('not saved mode')
    #     print('get bigram')
    #     tok = nltk.word_tokenize(data)
    #     bi_fdist, bigrams = get_ngram(tok, 2)
    #     print('get trigram')
    #     tri_fdist, tri_grams = get_ngram(tok, 3)
    #     # print('get fourgram')
    #     # four_fdist, four_grams = get_ngram(tok, 4)
    #     # print('get fivegram')
    #     # five_fdist, five_grams = get_ngram(tok, 5)
    #     print('convert to list - tri')
    #     tri_flist = tri_fdist.most_common(len(tri_fdist))
    #     print('convert to list - four')
    #     # four_flist = four_fdist.most_common(len(four_fdist))
    #     # print('convert to list - five')
    #     # five_flist = five_fdist.most_common(len(five_fdist))
    #     print('ngram_to_bigram_LR(3, tri_flist)')
    #     toRight_tri2bi, toLeft_tri2bi = ngram_to_bigram_LR(3, tri_flist)
    #     print('ngram_to_bigram_LR(4, four_flist)')
    #     # toRight_four2bi, toLeft_four2bi = ngram_to_bigram_LR(4, four_flist)
    #     # print('ngram_to_bigram_LR(5, five_flist)')
    #     # toRight_five2bi, toLeft_five2bi = ngram_to_bigram_LR(5, five_flist)
    #     # print('fivegrams_middle_predict(5, five_flist)')
    #     # fivegrams_middle = fivegrams_middle_predict(5, five_flist)
    #     print('word2vec training')
    #     word_model = gensim.models.Word2Vec(sentences, size=300, min_count=2, window=5, workers=10, iter=100)
    #     word_model.save('word2vecData.model')
    #     print('saving')
    #     with open('toRight_tri2bi.bin', 'wb') as f:
    #         pickle.dump(toRight_tri2bi, f, pickle.HIGHEST_PROTOCOL)
    #     print('saving')
    #     with open('toLeft_tri2bi.bin', 'wb') as f:
    #         pickle.dump(toLeft_tri2bi, f, pickle.HIGHEST_PROTOCOL)
    #     print('saving')
    #     # with open('toRight_four2bi.bin', 'wb') as f:
    #     #     pickle.dump(toRight_four2bi, f, pickle.HIGHEST_PROTOCOL)
    #     # print('saving')
    #     # with open('toLeft_four2bi.bin', 'wb') as f:
    #     #     pickle.dump(toLeft_four2bi, f, pickle.HIGHEST_PROTOCOL)
    #     # print('saving')
    #     # with open('toRight_five2bi.bin', 'wb') as f:
    #     #     pickle.dump(toRight_five2bi, f, pickle.HIGHEST_PROTOCOL)
    #     # print('saving')
    #     # with open('toLeft_five2bi.bin', 'wb') as f:
    #     #     pickle.dump(toLeft_five2bi, f, pickle.HIGHEST_PROTOCOL)
    #     # print('saving')
    #     # with open('fivegrams_middle.bin', 'wb') as f:
    #     #     pickle.dump(fivegrams_middle, f, pickle.HIGHEST_PROTOCOL)
    #     print('END')

        # toRight : X, Y 나오고 그 다음에 나올 것
        # toLeft : A, X , Y 에서 X, Y 나왔을 때 A 에 올것.

if __name__ == "__main__":
    main(True)
