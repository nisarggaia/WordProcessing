import getpass, imaplib
from flanker import mime
import email as em2
import json
from textblob import TextBlob as tb
import nltk
import re
import base64
from bs4 import BeautifulSoup


# Function to get the word count
def tf(word, blob):
    if words.has_key(word):
        wCount = words.get(word)
        wCount = wCount + blob.words.count(word)
        words[word] = wCount
    else:
        words[word] = blob.words.count(word)
    return words

# Connecting to IMAP Server and logging in
M = imaplib.IMAP4_SSL("imap.gmail.com", 993)
email = raw_input("Email address: ")
password = getpass.getpass()
M.login(email, password)


M.select()


# Searching/Fetching the emails from the inbox
typ, data = M.search(None, 'SUBJECT', "Welcome!")
#typ, data = M.fetch(data[0], '(RFC822)')
#emailbody = data[0][1]
#msg2 = em2.message_from_string(emailbody)
#mailString = str(data[0][1])
#listOfEmails = [[]]


def clean_html(html):
    # First we remove inline JavaScript/CSS:
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
    # Then we remove html comments. This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
    # Next we can remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
    # Finally, we deal with whitespace
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    return cleaned.strip()
# Storing the information from the email. From, To, Date, CC, Body and Word Count in the body
emailDict = {}
with open('./eData2.json', 'w') as f:
    for num in data[0].split():
        emailInfo = {}
        typ, data = M.fetch(num, '(RFC822)')
        emailbody = data[0][1]
        msg2 = em2.message_from_string(emailbody)
        mailString = str(data[0][1])
        msg = mime.from_string(mailString)
        n = int(num)
        n = n-1
        #print n
        if msg2.is_multipart():
            for payload in msg2.get_payload():
                raw = BeautifulSoup(payload.get_payload(decode=True), 'html.parser').get_text()
                #print raw
        else:
            raw = BeautifulSoup(msg2.get_payload(decode=True), 'html.parser').get_text()
            #print raw
        #print type(msg.parts)
        #if type(msg.parts) == list:
        #    continue
        #else:
        #a = msg.parts[1].body
            #if a is not None:
            #print type(a)
            #raw = clean_html(msg.parts[1].body)
            #raw = BeautifulSoup(msg.parts[1].body, 'html.parser').get_text().encode('ascii', 'replace')
        tokens = nltk.word_tokenize(raw)
        posTag = nltk.pos_tag(tokens)
        for word in posTag:
            if word[1] == 'NNP':
                print word[0]
        emailInfo['from'] = msg2['From']
        emailInfo['date'] = msg2['Date']
        emailInfo['to'] = msg2['To']
        emailInfo['cc'] = msg2['Cc']
                #emailInfo['body'] = msg.parts[0].body
        #a.encode('ascii', 'replace')
        #tBlob = tb(a)
        #words = {}
        #for word in tBlob.words:
         #   tf(word, tBlob)
        #emailInfo['wCount'] = words
            #else:
                #continue
        emailDict[n] = emailInfo
        print '-----------------------------------------------------------------------------'

    json.dump(emailDict, f, indent=4, separators=(',', ':'))

print len(emailDict)
f.close()
#for part in msg.parts:
 #   print 'Content-Type: {}'.format(part), part.body


#msg = mime.from_string(mailString)
#for part in msg2.walk():
#    print part.get_content_type()
#print msg.headers.items()


M.close()
M.logout()