#!/usr/bin python
# -*- coding: utf-8 -*-

import amazon_keys

from amazonproduct import API, AWSError

import re
import time
import csv


class AmazonMovies(object):
    def __init__(self, titles):
        self._api = API(cfg=amazon_keys.config)
        self._input_movies = self.get_movie_dict(titles)
        self.movies_dict = self.get_similarproducts(self._input_movies)
        self.movies = self.get_titles(self.movies_dict)

    def get_movie_dict(self, titles):
        tmp_list = []
        for title in titles:
            tmp_list.append({'title': title, 'asin': self.get_asin(title)})
        return tmp_list

    def get_asin(self, title):
        time.sleep(2)  # 1.8sのインターバルあれば制限に引っかからない？

        asin = u""
        try:
            for items in self.api.item_search('DVD', Keywords=title, limit=1):
                for item in items:
                    asin = unicode(item.ASIN)
                    break
                break
        except AWSError, e:
            print("code:%s message:%s" % (e.code, e.message))

        return asin

    def get_similarproducts(self, movies):
        tmplist = []
        for i, movie in enumerate(movies):
            print "(%d/%d) Search: %s" % (i+1, len(movies), movie['title'])
            time.sleep(2)  # 1.8sのインターバルあれば制限に引っかからない？

            similars = []
            try:
                res = self.api.similarity_lookup(movie['asin'])
                for item in res.Items.Item:
                    tmplist.append(unicode(item.ItemAttributes.Title))
            except AWSError, e:
                print("code:%s message:%s" % (e.code, e.message))

            movie['similars'] = similars
            tmplist.append(movie)
        return tmplist

    def save_movies(self, path="AmazonRecommendMovies.csv"):
        output_dict = []
        for movie in self.movies:
            for similar in movie['similars']:
                output_dict.append({
                    'asin': movie['asin'],
                    'title': movie['title'],
                    'similar': similar
                })

        params = ['asin', 'title', 'similar']
        header = dict([(v, v) for v in params])
        output_dict.insert(0, header)
        with open(path, 'wb') as fd:
            writer = csv.DictWriter(fd, params, extrasaction='ignore')
            writer.writerows(output_dict)
        return

    def get_titles(self, movies):
        tmp_list = []
        for movie in movies:
            for similar in movie['similars']:
                tmp_list.append(self.normalize_title(similar))
        return list(set(tmp_list))

    def normalize_title(self, title):
        patrn1 = re.compile(r"(\[.*\]|\(.*\)|【.*】|<.*>|（.*）|〔.*〕)")
        patrn2 = re.compile(r"(DVD|Blu-ray|ブルーレイ|枚組).*")
        patrn3 = re.compile(r"\s.*(MovieNEX|2D|3D|エディション|ディスク|特別(編|版)).*")
        patrn4 = re.compile(r"\s$")

        tmp = patrn1.sub("", title)
        tmp = patrn2.sub("", tmp)
        tmp = patrn3.sub("", tmp)
        tmp = patrn4.sub("", tmp)

        return tmp
