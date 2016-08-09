import getpass, imaplib
from flanker import mime
import email as em2
import json
from textblob import TextBlob as tb


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
typ, data = M.search(None, "ALL")
#typ, data = M.fetch(data[0], '(RFC822)')
#emailbody = data[0][1]
#msg2 = em2.message_from_string(emailbody)
#mailString = str(data[0][1])
#listOfEmails = [[]]

# Storing the information from the email. From, To, Date, CC, Body and Word Count in the body
emailDict = {}
with open('./eData.json', 'w') as f:
    for num in data[0].split():
        emailInfo = {}
        typ, data = M.fetch(num, '(RFC822)')
        emailbody = data[0][1]
        msg2 = em2.message_from_string(emailbody)
    #print('Message %s\n%s\n' % (num, data[0][1]))
        mailString = str(data[0][1])
    #print type(mailString)
        msg = mime.from_string(mailString)
        n = int(num)
        n = n-1
    #print n
    #print msg.headers['Date']
    #if n==5:
    #    print msg.parts[0].body

    #l = [msg.headers['From'], msg.headers['Date'], msg.headers['To'], msg.headers['Cc']]
        #print msg.headers['Date']
    #print mailString
        if type(msg.parts) == list:
            continue
        else:
            a = msg.parts[0].body
            if a is not None:
                emailInfo['from'] = msg.headers['From']
                emailInfo['date'] = msg.headers['Date']
                emailInfo['to'] = msg.headers['To']
                emailInfo['cc'] = msg.headers['Cc']
                emailInfo['body'] = msg.parts[0].body
                a.encode('ascii', 'replace')
                tBlob = tb(a)
                words = {}
                for word in tBlob.words:
                    tf(word, tBlob)
                emailInfo['wCount'] = words
            else:
                continue
            emailDict[n] = emailInfo

    json.dump(emailDict, f, indent=4, separators=(',', ':'))

print len(emailDict)
f.close()
        #for part in msg.parts:
         #   print 'Content-Type: {}'.format(part)


#msg = mime.from_string(mailString)
#for part in msg2.walk():
#    print part.get_content_type()
#print msg.headers.items()


M.close()
M.logout()