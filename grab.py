# coding=utf-8
import requests
from pprint import pprint
import nltk
import langid
import codecs
from tqdm import tqdm

output_file = 'romantyzm.txt'

endpoint = 'http://wolnelektury.pl/api/epochs/romantyzm/books/'

response = requests.get(endpoint)

contents = [x['href'] for x in response.json()]
pprint(contents)
allbooks = len(contents)
print "Found books: ", allbooks

def extract_text(url):

    raw = requests.get(url).text

    lang = langid.classify(raw)[0]
    #print lang
    if lang != 'pl' or raw.startswith('Adomas'):
        #print 'Not polish, omitting'
        return ''

    idx = raw.find(u'-----\r\nTa lektura, podobnie jak tysiące ')
    startidx = raw.find('\r\n'*3)

    assert startidx != -1
    meat = raw[startidx+6:idx]

    meat = meat.replace(u'\r\n', '\n')
    return meat

counter = 1

with codecs.open(output_file, 'w', encoding='utf-8') as f:
    for c in tqdm(contents):
        #print counter, '/', allbooks
        counter += 1
        r = requests.get(c).json()
        txturl = r['txt']
        if txturl == '':
            continue
        tqdm.write(txturl)
        txt = requests.get(txturl)
        f.write(extract_text(txturl))
