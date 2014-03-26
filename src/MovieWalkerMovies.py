#!/usr/bin python
# -*- coding: utf-8 -*-

import requests
from pyquery import PyQuery as pq

import csv
import time


class MovieWalkerMovies(object):
    def __init__(self):
        self._TargetURL = "http://movie.walkerplus.com/list/2013"
        self.movies_dict = self.get_movies()
        self.movies = self.get_titles(self.movies_dict)

    def get_movies(self):
        tmp_list = []
        for i in range(1, 13):
            try:
                r = requests.get("%s/%02d/" % (self._TargetURL, i))
            except requests.exceptions.RequestsException as e:
                print str(e)
                return

            q = pq(r.text)
            for g in q('div#personMovieList').children('.hiraganaGroup'):
                tmp = pq(g)
                date = tmp('div.hiragana').text()
                for m in tmp('.movies').children('.movie'):
                    tmptmp = pq(m)
                    tmp_list.append({
                        "date": date.encode('utf-8'),
                        "title": tmptmp('h3').text().encode('utf-8')
                    })
            time.sleep(0.05)
        print "get %d movies" % len(tmp_list)
        return tmp_list

    def get_titles(self, movies):
        tmplist = []
        for movie in movies:
            tmplist.append(movie['title'])
        return tmplist

    def save_movies(self, path="MovieWalkerMovies.csv"):
        params = ['date', 'title']
        header = dict([(v, v) for v in params])
        self.moviedict.insert(0, header)
        with open(path, 'wb') as fd:
            writer = csv.DictWriter(fd, params, extrasaction='ignore')
            writer.writerows(self.moviedict)
        return
