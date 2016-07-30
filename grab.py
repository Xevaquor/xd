# coding=utf-8

import requests
from pprint import pprint
import nltk
import langid
import pymongo

mongo = pymongo.MongoClient()

db = mongo.mickiewicz

books = db.books

mickiewicz = 'http://wolnelektury.pl/api/epochs/romantyzm/books/'

response = requests.get(mickiewicz)

contents = [x['href'] for x in response.json()]
pprint(contents)
allbooks = len(contents)
print "Found books: ", allbooks

def extract_text(url):
    print "Extracting from ", url

    raw = requests.get(url).text

    lang = langid.classify(raw)[0]
    print lang
    if lang != 'pl' or raw.startswith('Adomas'):
        print 'Not polish, omitting'
        return []

    idx = raw.find(u'-----\r\nTa lektura, podobnie jak tysiące ')
    startidx = raw.find('\r\n'*3)

    assert startidx != -1
    meat = raw[startidx+6:idx]

    meat = meat.replace(u'\r\n', '\n')

    books.insert({'text': meat})

    return nltk.word_tokenize(meat)

listoftokens = []
counter = 1

for c in contents:
    print counter, '/', allbooks
    counter += 1
    r = requests.get(c).json()
    txturl = r['txt']
    if txturl == '':
        continue
    pprint(txturl)
    txt = requests.get(txturl)
    listoftokens += extract_text(txturl)


setoftokens = sorted(list(set(listoftokens)))
tokens_to_idx = dict((c, i) for i, c in enumerate(setoftokens))
n_tokens = len(listoftokens)
n_vocab = len(setoftokens)

print n_tokens, ' tokens'
print n_vocab, ' vocabulary size'



