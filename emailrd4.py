from __future__ import division, unicode_literals
import getpass, imaplib
from flanker import mime
import email as em2
import json
import math
from itertools import islice
from textblob import TextBlob as tb

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def getImportant(eData, eachEmail):
    vw = get_weighted_vectors(eData)

def get_weighted_vectors(d):
    for (user, data) in d.iteritems():
        # Iterate through and normalize the each user vector.
        user_sum = sum([v for v in data.itervalues()])
        data.update((k, v/user_sum) for (k, v) in data.iteritems())

        # Now get the weighted vector values using inverse user frequency.
        data.update((k, config.tuning_param["alpha"] * v * get_inverse_user_freq(k, d))
                    for (k, v) in data.iteritems())

        d[user] = data
    return d

words = {}
def tf(word, blob):
    if words.has_key(word):
        wCount = words.get(word)
        wCount = wCount + blob.words.count(word)
        words[word] = wCount
    else:
        words[word] = blob.words.count(word)
    #return blob.words.count(word)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

with open('./eData.json') as data_file:
    eData = json.load(data_file)

#-------------------------------------------------------------------------------------------------------------------------
#print data
'''
bodyList = []
for dict in eData:
    a = eData[dict]['body']
    if a is not None:
        a.encode('ascii', 'replace')
        bodyList.append(tb(a))

print type(bodyList[1])
'''


#for body in bodyList:
#    for word in body:
#        print type(word)
'''
for i, blob in enumerate(bodyList):
    for word in blob.words:
        tf(word, blob)
    #print("Top words in document {}".format(i + 1))
    #scores = {word: tfidf(word, blob, bodyList) for word in blob.words}
    #sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    #for word, score in sorted_words[:3]:
        #print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))

'''

for (eachEmail, data) in eData.iteritems():
    getImportant(eData, eachEmail)
#

orderedWordList = sorted(words, key=words.__getitem__, reverse=True)
print take(3, orderedWordList)