#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import nltk
from nltk.corpus.reader import *
from nltk.corpus.reader.util import *
from nltk.text import Text

def JPCorpusReader(root, fieldids, encoding='utf-8'):
    sent_tokenizer = nltk.RegexpTokenizer(u'[^ 「」！？。]*[！？。]')
    chartype_tokenizer = nltk.RegexpTokenizer(u'([ぁ-んー]+|[ァ-ン]+|[\u4e00-\u9FFF]+|[^ぁ-んァ-ン\u4e00-\u9FFF]+)')
    corpus = PlaintextCorpusReader(root, fieldids,
            encoding = encoding,
            para_block_reader = read_line_block,
            sent_tokenizer = sent_tokenizer,
            word_tokenizer = chartype_tokenizer)
    return corpus

import re, pprint

def pp(obj):
    pp = pprint.PrettyPrinter(indent=4, width=160)
    str = pp.pformat(obj)
    return re.sub(r"\\u([0-9a-f]{4})", lambda x: unichr(int("0x"+x.group(1), 16)), str)


if __name__ == "__main__":
    corpus = JPCorpusReader("tmp/", "ginga.txt", "sjis")
    text = nltk.Text(corpus.words())
    freq = nltk.FreqDist(text)
    # ワードカウント
    #print "\n".join("%s\t%d" % (w,f) for w,f in freq.items()[:20])
    # 検索
    #text.concordance(u"苹果", 10, 5)
    # 類似
    #text.similar(u"カムパネルラ")
    # 自動生成
    # text.generate()