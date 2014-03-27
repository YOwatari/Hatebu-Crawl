#!/usr/bin python
# -*- coding: utf-8 -*-

import requests
from pyquery import PyQuery as pq
import re


class AcademyAward(object):
    def __init__(self, year):
        self._year = int(year)
        self._TargetURL = "http://ja.wikipedia.org/wiki/アカデミー作品賞"
        self.movies = []
        self.get_awardmovies()

    def get_awardmovies(self):
        patrn = re.compile("\s*\[\d+\]$")

        try:
            r = requests.get(self._TargetURL)
        except requests.exceptions.RequestsException as e:
            print "AcademyAward: " + str(e)
            return

        q = pq(r.text)
        for tbl in q("table.wikitable"):
            tbl = pq(tbl)
            try:
                year = int(tbl("caption big").text()[0:4])
            except:
                year = -1
            if year >= self._year:
                for tr in tbl("tr"):
                    title = pq(tr)("td:eq(0)").text()
                    if "" != title:
                        self.movies.append(patrn.split(title)[0])
        print "AcademyAward done."
        return

    def save_movies(self, path="AcademyAwardMovies.csv"):
        with open(path, 'wb') as fd:
            for movie in self.movies:
                fd.write(movie.encode('utf-8') + '\n')
        print "AcademyAward saved."
        return
