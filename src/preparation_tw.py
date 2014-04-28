#!/usr/bin python
# -*- coding:utf-8 -*-

import MeCab
import codecs
import glob
import re
import json

word_class = u"名詞"


def extractKeywords(input_text):
    tagger = MeCab.Tagger('-Ochasen')
    node = tagger.parseToNode(input_text.encode('utf-8'))

    keywords = []
    while node:
        if node.feature.split(",")[0] == word_class.encode('utf-8'):
            keywords.append(node.surface)
        node = node.next

    return keywords


def txt2csv(file):
    de = re.compile(r'(\d+8?9)')
    url = re.compile(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+')
    br = re.compile(r'\n')

    with codecs.open(file, "rb", "utf-8") as fd:
        text = fd.read()
        text = u''.join(url.split(text))
        text = u'\t'.join(br.split(text))
        tmp = []
        text = de.split(text)
        for i, v in enumerate(text):
            if i > 0 and i % 2 == 0:
                tmp.append(text[i-1] + text[i])
        text = u'\n'.join(list(set(tmp)))
        return text


def sameTweetCheck(filename):
    files = glob.glob(filename)
    textlist = []

    for f in files:
        textlist.append(txt2csv(f))

    p = re.compile(r'\d+,')
    txt = []
    for text in textlist:
        txt.append(p.sub('', text))

    p = re.compile(r'@|RT|:|;')
    return p.sub('', ''.join(txt))


def main(input, output):
    text = sameTweetCheck(input)

    tmp = []
    tmp = tmp + extractKeywords(text)

    tmpset = list(set(tmp))
    tmpdict = {}
    for v in tmpset:
        tmpdict[v] = 0
        for w in tmp:
            if v == w:
                tmpdict[v] += 1

    csvfile = open(output, 'wb')
    for k, v in sorted(tmpdict.items(), key=lambda x: x[1]):
        csvfile.writelines(k+','+str(v)+'\n')
    csvfile.close()

    # with open(output, "wb") as fd:
    #     fd.write(json.dumps(tmpdict, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    for i in xrange(207):
        main(u'tmp/中間発表/tw/'+unicode(i)+u'_*.txt', u'tmp/csv/'+unicode(i)+u'_output.csv')
