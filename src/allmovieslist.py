#!/usr/bin python
# -*- coding: utf-8 -*-

from AcademyAwardList import AcademyAward as AA

from amazonproduct import API, AWSError

import time
import csv

config = {
    'access_key': 'AKIAIQX64PSGVVCKSC3A',
    'secret_key': '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',
    'associate_tag': 'amazonsearch88-22',
    'locale': 'jp'
}


class AmazonList(object):
    def __init__(self, titles):
        self.movielist = []
        self.api = API(cfg=config)
        self.titles = titles
        self.GetMovieList(self.titles)

    def GetMovieList(self, titles):
        for i, title in enumerate(titles):
            print "(%d/%d) Search: %s" % (i+1, len(titles), title)
            tmp_asin = u""
            try:
                for items in self.api.item_search('DVD', Keywords=title, limit=1):
                    for item in items:
                        tmp_asin = unicode(item.ASIN)
                        break
                    break
            except AWSError, e:
                print("code:%s message:%s" % (e.code, e.message))
            time.sleep(2)  # 1.8sのインターバルあれば制限に引っかからない？

            tmplist = []
            try:
                res = self.api.similarity_lookup(tmp_asin)
                for item in res.Items.Item:
                    tmplist.append(unicode(item.ItemAttributes.Title))
            except AWSError, e:
                print("code:%s message:%s" % (e.code, e.message))
            time.sleep(2)  # 1.8sのインターバルあれば制限に引っかからない？

            self.movielist.append({'title': title, 'recommends': tmplist})

    def SaveMovieList(self):
        tmp_lines = []
        for movie in self.movielist:
            tmp = []
            tmp.append(movie['title'].encode('utf-8'))
            for recommend in movie['recommends']:
                tmp.append(recommend.encode('utf-8'))
            tmp_lines.append(tmp)
        with open('AmazonRecommendMovies.csv', 'wb') as fd:
            writer = csv.writer(fd, lineterminator='\n')
            writer.writerows(tmp_lines)

if __name__ == "__main__":
    academy = AA()
    amazon = AmazonList(academy.movielist)
    amazon.SaveMovieList()
    exit()
