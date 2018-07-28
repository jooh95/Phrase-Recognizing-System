#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

__author__ = 'maxim'

import numpy as np
import gensim
import string

from keras.callbacks import LambdaCallback
from keras.layers.recurrent import LSTM
from keras.layers.embeddings import Embedding
from keras.layers import Dense, Activation
from keras.models import Sequential
import nltk as nltk
from keras.utils.data_utils import get_file
import random, glob, os, pickle
from gensim.models import Word2Vec

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

def sample(preds, temperature=1.0):
  if temperature <= 0:
    return np.argmax(preds)
  preds = np.asarray(preds).astype('float64')
  preds = np.log(preds) / temperature
  exp_preds = np.exp(preds)
  preds = exp_preds / np.sum(exp_preds)
  probas = np.random.multinomial(1, preds, 1)
  return np.argmax(probas)

def generate_next(text, num_generated=10):
  # word_idxs = [word2idx(word) for word in text.lower().split()]
  word_idxs = []
  for word in text.lower().split():
    tmp_word_idx = word2idx(word)
    if tmp_word_idx == 'ERROR':
      return 'ERROR'
    word_idxs.append(tmp_word_idx)

  for i in range(num_generated):
    prediction = model.predict(x=np.array(word_idxs))
    idx = sample(prediction[-1], temperature=0.7)
    word_idxs.append(idx)
  return ' '.join(idx2word(idx) for idx in word_idxs)

def on_epoch_end(epoch, _):
  print('\nGenerating text after epoch: %d' % epoch)

  texts = [
    'deep convolutional'
  ]
  for l in range(10):
    tmp_list = random.choice(sentences)
    texts.append(random.choice(tmp_list))

  for text in texts:
    sample = generate_next(text)
    if sample == 'ERROR':
      print("Out of Vocab Error")
    print('%s... -> %s' % (text, sample))

def main(isSaved = False):
  print('\nFetching the text...')
  # url = 'https://raw.githubusercontent.com/maxim5/stanford-tensorflow-tutorials/master/data/arxiv_abstracts.txt'
  # path = get_file('arxiv_abstracts.txt', origin=url)


  docs = ""
  os.chdir("./next_data")
  for file in glob.glob("*.txt"):
    docs += open(file, encoding='utf-8').read().lower()
  print('\nPreparing the sentences...')
  max_sentence_len = 361

  tmp_sentences = docs.split('\n')
  global sentences
  sentences = [[word for word in nltk.word_tokenize(sentence_one)] for sentence_one in tmp_sentences]



  print('Num sentences:', len(sentences))
  print('max_len', max_sentence_len)
  print('\nTraining word2vec...')
  global word_model
  # word_model= gensim.models.Word2Vec(sentences, size=300, min_count=2, window=5,workers=10, iter=100)
  # word_model.save('word2vecData.model')
  word_model = Word2Vec.load('word2vecData.model')
  pretrained_weights = word_model.wv.syn0
  vocab_size, emdedding_size = pretrained_weights.shape
  print('Result embedding shape:', pretrained_weights.shape)
  print('Checking similar words:')
  for word in ['we']:
    most_similar = ', '.join('%s (%.2f)' % (similar, dist) for similar, dist in word_model.most_similar(word)[:8])
    print('  %s -> %s' % (word, most_similar))



  print('\nPreparing the data for LSTM...')
  train_x = np.zeros([len(sentences)+10, max_sentence_len], dtype=np.int32)
  print(train_x.shape)
  train_y = np.zeros([len(sentences)+10], dtype=np.int32)
  print(train_y.shape)

  for i, sentence in enumerate(sentences):
    for t, word in enumerate(sentence[:-1]):
      try:
        train_x[i, t] = word2idx(word)
      except:
        print("ERROR (i)", i)
        print("ERROR (t)", t)
        print("ERROR (word)", word)

    try:
      train_y[i] = word2idx(sentence[-1])
    except:
      print(i)
  print('train_x shape:', train_x.shape)
  print('train_y shape:', train_y.shape)

  print('\nTraining LSTM...')
  global model
  model = Sequential()
  print('Embedding')
  model.add(Embedding(input_dim=vocab_size, output_dim=emdedding_size, weights=[pretrained_weights]))
  print('set LSTM Cell')
  model.add(LSTM(units=emdedding_size))
  print('set dense layer')
  model.add(Dense(units=vocab_size))
  print('activation function = softmax')
  model.add(Activation('softmax'))
  print('adam optimizer & loss = sparse_categorical_crossentropy')
  model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

  model.fit(train_x, train_y,
            batch_size=128,
            epochs=20,
            callbacks=[LambdaCallback(on_epoch_end=on_epoch_end)])
  model.save('word2vec_lstm_gen.model')
if __name__ == '__main__':
  main(False)