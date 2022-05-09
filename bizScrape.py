import urllib.request
import json
import re


#set dir to directory containing bizScrape.py
dir = ''
url = 'https://a.4cdn.org/biz/catalog.json'

response = urllib.request.urlopen(url).read()
threadCatalog = json.loads(response)
frontPage = threadCatalog[0]['threads']

filterTerms = ['BITCOIN', 'ATOM', '$ATOM', 'COSMOS', 'DVPN', '$DVPN', 'IRIS', '$IRIS', 'KAVA', '$KAVA', 'JUNO', '$JUNO',
               'MOVR', '$MOVR', 'KSM', '$KSM', 'Arbitrum', 'ADA', '$ADA', 'DOT', '$DOT', 'KSM', '$KSM', 'AVAX', 'PULSECHAIN', '$PLS', 'PLS', 'FTM', '$FTM', 'RLC', 'gem', 'ecosystem', '100x', 'ampleforth', 'general', 'metaverse', 'web3', 'web3/metaverse']
filterTerms = list((map(lambda x: x.lower(), filterTerms)))

matches = []
pattern = r'[\n]'
f = open(dir + '/scrapeResults.txt', 'a+')

for line in f:
    if line != '\n':
        matches.append(re.sub(pattern, '', line).strip().encode('utf-8'))

f.truncate(0)

for page in threadCatalog: 
    for thread in page['threads']:
        try:
            threadSubject = thread['sub'].lower().split()
            check = any(item in threadSubject for item in filterTerms)
            if check:
                    hyperlink = 'https://boards.4channel.org/biz/thread/%s' % thread['no']
                    subject = thread['sub']
                 
                    
                    matches.insert(0, hyperlink)
                    matches.insert(0, subject)
        except KeyError:
            pass

newMatchesList = []
counter = 0
print(matches)
# problem with script is that if two threads with same title exist, then everything fucks up
for i in matches:
    if i not in newMatchesList:
        counter += 1
        newMatchesList.append(i)
        newMatchesList.append('\n')
        if counter == 2:
            counter = 0
            newMatchesList.append('\n')

f = open(dir + '/scrapeResults.txt', 'a+')
for line in newMatchesList:
    f.write(line)

f.close()
