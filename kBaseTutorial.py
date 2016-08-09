import sqlite3
import time
import urllib2
from urllib2 import urlopen
import re
import cookielib
from cookielib import CookieJar
import datetime

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent','Mozilla/5.0')]

conn = sqlite3.connect('kBase.db')
c = conn.cursor()

def huffRSSvisit():
    try:
        page = "http://www.huffingtonpost.com/feeds/index.xml"
        sourceCode = opener.open(page).read()
        try:
            links = re.findall(r'<link>(.*?)</link>', sourceCode)
            for link in links:
                if link =="www.huffingtonpost.com":
                    pass
                else:
                    print 'visiting the link'
                    print '###############'
                    linkSource = opener.open(link).read()
                    linesOfInterest = re.findall(r'<p>(.*?)</p>',str(linkSource))
                    print 'Content'
                    for eachLine in linesOfInterest:
                        if '<img width>' in eachLine:
                            pass
                        elif '<a href=' in eachLine:
                            pass
                        else:
                            print eachLine

                    time.sleep(5)

        except Exception, e:
            print 'Failed second loop of huff visit'
            print str(e)

    except Exception, e:
        print 'Failed main loop of huff visit'
        print str(e)


huffRSSvisit()