#!/usr/bin python
# -*- coding: utf-8 -*-

import requests
from pyquery import PyQuery as pq
import csv
import time

TargetURL = "http://movie.walkerplus.com/list/2013"

if __name__ == "__main__":
    movielist = []

    for i in range(1, 13):
        try:
            r = requests.get("%s/%02d/" % (TargetURL, i))
        except requests.exceptions.RequestsExecption as e:
            print str(e)

        q = pq(r.text)
        for g in q('div#personMovieList').children('.hiraganaGroup'):
            tmp = pq(g)
            date = tmp('div.hiragana').text()
            for m in tmp('.movies').children('.movie'):
                tmptmp = pq(m)
                movielist.append({
                    "date": date.encode('utf-8'),
                    "title": tmptmp('h3').text().encode('utf-8')
                })
        time.sleep(0.05)

    params = ['date', 'title']
    header = dict([(v, v) for v in params])
    movielist.insert(0, header)
    with open('movies.csv', 'wb') as fd:
        writer = csv.DictWriter(fd, params, extrasaction='ignore')
        writer.writerows(movielist)

    exit()
