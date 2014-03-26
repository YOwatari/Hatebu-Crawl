#!/usr/bin python
# -*- coding: utf-8 -*-

import requests
from pyquery import PyQuery as pq
import csv
import time


class MovieWalkerList(object):
    def __init__(self):
        self.moviedict = []
        self.TargetURL = "http://movie.walkerplus.com/list/2013"
        self.GetMovieDict()

    def GetMovieDict(self):
        for i in range(1, 13):
            try:
                r = requests.get("%s/%02d/" % (self.TargetURL, i))
            except requests.exceptions.RequestsException as e:
                print str(e)
                return

            q = pq(r.text)
            for g in q('div#personMovieList').children('.hiraganaGroup'):
                tmp = pq(g)
                date = tmp('div.hiragana').text()
                for m in tmp('.movies').children('.movie'):
                    tmptmp = pq(m)
                    self.moviedict.append({
                        "date": date.encode('utf-8'),
                        "title": tmptmp('h3').text().encode('utf-8')
                    })
            time.sleep(0.05)
        print "get %d movies" % len(self.moviedict)

    def GetTitleList(self):
        tmplist = []
        for m in self.moviedict:
            tmplist.append(m['title'])
        return tmplist

    def SaveMovieDict(self):
        params = ['date', 'title']
        header = dict([(v, v) for v in params])
        self.moviedict.insert(0, header)
        with open('movies.csv', 'wb') as fd:
            writer = csv.DictWriter(fd, params, extrasaction='ignore')
            writer.writerows(self.moviedict)
        print "saved."

if __name__ == "__main__":
    mwl = MovieWalkerList()
    mwl.SaveMovieDict()
    exit()
