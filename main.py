# -*- coding: utf-8 -*-

import re
import codecs

print("Bib Label Generator")
filePathRead = input("Input un-labeled Bib file name:")
filePathWrite = input("Input the file name for labeled Bib file: ")
#filePathRead = 'ppg.bib'
#filePathWrite = 'ref.bib'
fileRead = codecs.open(filePathRead, 'r', encoding='utf-8')
#fileRead = open(filePathRead, 'r')
fileWrite = open(filePathWrite, 'w', encoding='utf-8')

entryHeader = '(@.*{).*\r+\n+$'
entryContent = '.*\s*=\s*{.*}.*\r+\n+$'
entryEnd = '.*}\r+\n+$'

regAuthorList = '\s*author\s*=\s*{(.*)}.*\r+\n+$'
regAuthor = '[[\S*\s]*,[\s\S*]*\sand\s]*[\S*\s]*,[\s\S*]*\r+\n+$'
regYear = '\s*year\s*=\s*{(\d{4})}.*\r+\n+$'
regTitle = '\s*title\s*=\s*{(.*)}.*\r+\n+$'
done = False

while done == False:
    rl = fileRead.readline()
    if rl == '':
        done = True
    else:
        done = False
    rl = rl.replace(u'\ufeff','')
    if re.match(entryHeader, rl):
        contentFlag = 'entryBegin'
        whead = re.match(entryHeader, rl).group(1)
        wbody = ''
    elif re.match(entryContent, rl):
        contentFlag = 'entryContent'
        wbody = wbody + rl
        
        result = re.match(regAuthorList, rl)
        if result:
            authorList = result.group(1)
            result = re.split('\sand\s', authorList)[0]
            if result:
                author = re.split('\s?,\s?', result)[0]
                if result:
                    author = re.split('\s*', author)[0]

        result = re.match(regTitle, rl)
        if result:
            title = result.group(1)

        result = re.match(regYear, rl)
        if result:
            year = result.group(1)

    elif re.match(entryEnd, rl):
        contentFlag = 'entryEnd'
        #Get all the words in the title
        titleWordList = re.split('\s+', title)
        #Exclude the words like The, the, A, a
        for titleWord in titleWordList:
            if not re.match('^([T|t]he|A|a)$', titleWord):
                titleLabel = titleWord
                break
        #If there is no meaningful word found, use the first available word in the title
        if not titleWord:
            titleLabel = titleWordList[0]
        #Generate the label
        label = author + year + titleLabel 
        #Generate the body part
        wbody = wbody + rl
        toWrite = whead.replace('\r\n','') + label + '\r\n' + wbody + '\r\n'
        toWrite = toWrite.replace('\r\n', '\n')
        fileWrite.write(toWrite)
    else:
        contentFlag = 'illegal' 

fileWrite.close()

#commit from vsc