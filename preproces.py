# coding=utf-8

import requests
from pprint import pprint
import nltk
import langid
import pymongo
import numpy as np
import pickle

mongo = pymongo.MongoClient()

db = mongo.mickiewicz

books = db.books

listoftokens = []

for b in books.find()[:2]:
    listoftokens += nltk.word_tokenize(b[u'text'])


setoftokens = sorted(list(set(listoftokens)))
tokens_to_idx = dict((c, i) for i, c in enumerate(setoftokens))
n_tokens = len(listoftokens)
n_vocab = len(setoftokens)
idx_to_tokens = dict((i, c) for i, c in enumerate(setoftokens))

print n_tokens, ' tokens'
print n_vocab, ' vocabulary size'
print listoftokens


def to_categorical(y, nb_classes=None):
    '''Convert class vector (integers from 0 to nb_classes)
    to binary class matrix, for use with categorical_crossentropy.
    '''
    if not nb_classes:
        nb_classes = np.max(y)+1
    Y = np.zeros((len(y), nb_classes))
    for i in range(len(y)):
        Y[i, y[i]] = 1.
    return Y

seq_length = 10
dataX = []
dataY = []
for i in range(0, n_tokens - seq_length, 1):
	seq_in = listoftokens[i:i + seq_length]
	seq_out = listoftokens[i + seq_length]
	dataX.append([tokens_to_idx[char] for char in seq_in])
	dataY.append(tokens_to_idx[seq_out])
n_patterns = len(dataX)
print "Total Patterns: ", n_patterns
# reshape X to be [samples, time steps, features]
X = np.reshape(dataX, (n_patterns, seq_length, 1))
# normalize
X = X / float(n_vocab)
# one hot encode the output variable
y = to_categorical(dataY)

np.save('x', X)
np.save('y', y)

with open('setoftokens.pickle', 'wb') as handle:
  pickle.dump(setoftokens, handle)
with open('n_tokens.pickle', 'wb') as handle:
  pickle.dump(n_tokens, handle)
with open('tokens_to_idx.pickle', 'wb') as handle:
  pickle.dump(tokens_to_idx, handle)
with open('n_vocab.pickle', 'wb') as handle:
  pickle.dump(n_vocab, handle)
with open('idx_to_tokens.pickle', 'wb') as handle:
  pickle.dump(idx_to_tokens, handle)


setoftokens = sorted(list(set(listoftokens)))
tokens_to_idx = dict((c, i) for i, c in enumerate(setoftokens))
n_tokens = len(listoftokens)
n_vocab = len(setoftokens)
idx_to_tokens = dict((i, c) for i, c in enumerate(setoftokens))