#!/usr/bin python
# -*- coding:utf-8 -*-

import MeCab
import codecs

input_text = u"Mecabちゃんに形態素解析してもらうんだよ．"

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


if __name__ == "__main__":
    tmp = []
    with codecs.open("input.txt", "rb", "utf-8") as fd:
        tmp = tmp + extractKeywords(fd.read())

    tmpset = list(set(tmp))

    tmpdict = {}
    for v in tmpset:
        tmpdict[v] = 0
        for w in tmp:
            if v == w:
                tmpdict[v] += 1

    for k,v in sorted(tmpdict.items(), key=lambda x:x[1]):
        print k,v