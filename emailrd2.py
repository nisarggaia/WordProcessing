import getpass, imaplib
from flanker import mime
import email as em2
import json
import nltk
import re
#import base64
from talon import signature
#import talon
from bs4 import BeautifulSoup

#talon.init()

def clean_html(html):
    # First we remove inline JavaScript/CSS:
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
    # Then we remove html comments. This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->?", "", cleaned)
    # Next we can remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
    # Finally, we deal with whitespace
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    cleaned = re.sub(r"[+|@]", " ", cleaned)
    return cleaned.strip()

# Connecting to IMAP Server and logging in
M = imaplib.IMAP4_SSL("imap.gmail.com", 993)
email = raw_input("Email address: ")
password = getpass.getpass()
M.login(email, password)
M.select()

# Searching/Fetching the emails from the inbox
#typ, data = M.search(None, 'SUBJECT', "latest activity")
typ, data = M.search(None, "ALL")

# Storing the information from the email. From, To, Date, CC, Body and Word Count in the body
emailDict = {}
with open('./eData.json', 'w') as f:
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
        #print type(msg2)
        if msg2.is_multipart():
            for payload in msg2.get_payload():
                if type(payload.get_payload())==list:
                    continue
                if payload.get_payload(decode=True) is None:
                    continue
                else:
                    print type(payload.get_payload())
                    raw = BeautifulSoup(payload.get_payload(decode=True), 'lxml').get_text()
                #print raw
        else:
            #raw = BeautifulSoup(msg2.get_payload(decode=True), 'html.parser').get_text()
            raw = BeautifulSoup(payload.get_payload(decode=True), 'lxml').get_text()

        links = re.findall(r'((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', raw)
        print msg2['Date']
        #text, sign = signature.extract(raw, msg2['From'])
        #print text
        #print type(sign)
        tokens = nltk.word_tokenize(raw)
        posTag = nltk.pos_tag(tokens)
        eWords = {}
        i=0
        for word in posTag:
            if word[1] == 'NNP':
                eWords[i] = word[0]
                i=i+1
                #print word[0]
        #print len(eWords)
        eLinks = {}
        if links:
            j=0
            for link in links:
                eLinks[j] = link[0]
                j = j+1
        emailInfo['from'] = msg2['From']
        emailInfo['date'] = msg2['Date']
        emailInfo['to'] = msg2['To']
        emailInfo['cc'] = msg2['Cc']
        emailInfo['Links'] = eLinks
        emailInfo['Words'] = eWords
        emailDict[n] = emailInfo
        print '-----------------------------------------------------------------------------'

    json.dump(emailDict, f, indent=4, separators=(',', ':'))

print len(emailDict)
f.close()

M.close()
M.logout()