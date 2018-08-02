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

global afdata
afdata = {};

def get_ngram(text, n):
    print("get_ngram()")
    filename = str(n) + "grams" +".pickle"
    print("tokenizing")
    tok = nltk.word_tokenize(text)
    print("trigrams")
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
    data = fdist.most_common(5000)
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

def main():
    isSaved = True

    if isSaved == True:
        os.chdir("./next_data")
        global tri_fdist
        global bi_fdist
        tri_fdist = get_ngrams_saved(3)
        bi_fdist = get_ngrams_saved(2)
    else:
        data = ""
        #     os.chdir("./next_data")
        for file in glob.glob("*.txt"):
            data += open(file, encoding='utf-8').read().lower()
        #     get_ngram(data,2)

        fdist, ngrams = get_ngram(data, 3)
        bi_fdist, bigrams = get_ngram(data, 2)
    tri_flist = tri_fdist.most_common(len(tri_fdist))
    tri_dict_data = create_ngram_dict(tri_flist, 3, 50)
    toRight, toLeft = trigram_to_bigram_LR(tri_flist)
    # toRight : X, Y 나오고 그 다음에 나올 것
    # toLeft : A, X , Y 에서 X, Y 나왔을 때 A 에 올것.
if __name__ == '__main__':
    main()