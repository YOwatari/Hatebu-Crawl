#!/usr/bin python
# -*- coding: utf-8 -*-

import amazon_keys

from amazonproduct import API, AWSError

import re
import time
import csv


class AmazonMovies(object):

    def __init__(self, titles):
        self._pattern1 = re.compile(r"(\[.*\]|\(.*\)|【.*】|<.*>|（.*）|〔.*〕)")
        self._pattern2 = re.compile(r"(DVD|Blu-ray|ブルーレイ|枚組).*")
        self._pattern3 = re.compile(r"\s.*(MovieNEX|2D|3D|エディション|ディスク|特別(編|版)).*")
        self._pattern4 = re.compile(r"\s$")

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
            for items in self._api.item_search('DVD', Keywords=title, limit=1):
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
            print "(%d/%d) %s" % (i+1, len(movies), movie['title'])
            time.sleep(2)  # 1.8sのインターバルあれば制限に引っかからない？

            similars = []
            try:
                res = self._api.similarity_lookup(movie['asin'])
                for item in res.Items.Item:
                    similars.append(unicode(item.ItemAttributes.Title))
            except AWSError, e:
                print("code:%s message:%s" % (e.code, e.message))

            movie['similars'] = similars
            tmplist.append(movie)
        return tmplist

    def save_movies(self, path="AmazonRecommendMovies.csv"):
        output_dict = []
        for movie in self.movies_dict:
            for similar in movie['similars']:
                output_dict.append({
                    'asin': movie['asin'].encode('utf-8'),
                    'title': movie['title'].encode('utf-8'),
                    'similar': similar.encode('utf-8')
                })

        params = ['asin', 'title', 'similar']
        header = dict([(v, v) for v in params])
        output_dict.insert(0, header)
        with open(path, 'wb') as fd:
            writer = csv.DictWriter(fd, params, extrasaction='ignore')
            writer.writerows(output_dict)
        print "AmazonMovies saves"
        return

    def get_titles(self, movies):
        titles = []
        for movie in movies:
            for similar in movie['similars']:
                titles.append(self.normalize_title(similar))
        return list(set(titles))

    def normalize_title(self, title):
        tmp = self._pattern1.sub("", title)
        tmp = self._pattern2.sub("", tmp)
        tmp = self._pattern3.sub("", tmp)
        tmp = self._pattern4.sub("", tmp)
        return tmp
