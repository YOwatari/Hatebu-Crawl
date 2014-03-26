#!/usr/bin python
# -*- coding: utf-8 -*-

import requests
from pyquery import PyQuery as pq
import twitter
import time
import re
import csv

TargetURL = "http://ja.wikipedia.org/wiki/アカデミー作品賞"
SaveFilePath = "AcademyAwardList.csv"

patrn = re.compile("\s*\[\d+\]$")


class AcademyAward(object):
    def __init__(self):
        self.movielist = []
        self.GetAwardList()

    def GetAwardList(self):
        try:
            r = requests.get(TargetURL)
        except requests.exceptions.RequestsException as e:
            print str(e)

        q = pq(r.text)

        for tbl in q("table.wikitable"):
            tbl = pq(tbl)
            try:
                year = int(tbl("caption big").text()[0:4])
            except:
                year = -1
            if year >= 2010:
                for tr in tbl("tr"):
                    title = pq(tr)("td:eq(0)").text()
                    if "" != title:
                        self.movielist.append(patrn.split(title)[0])


def main():
    aa = AcademyAward()
    ml = aa.movielist
    #tw = TwitterCrawler(myapp_apikeys)
    print len(ml)
    # csvlist = []
    # for i in xrange(0, len(ml)):
    #     tmplist = []
    #     tmplist.append(ml[i].encode('utf-8'))
    #     for j in xrange(0, len(ml)):
    #         if j <= i:
    #             tmplist.append(0)
    #             continue
    #         q = ml[i] + "+" + ml[j]
    #         print "searching... %s" % q
    #         time.sleep(5.0)  # 180times/15minutes = 1times/5s
    #         twl = tw.search(q)
    #         tmplist.append(len(twl))
    #         with open('aa/'+q+'.txt', 'wb') as fd:
    #             [fd.write(t.text.encode('utf-8')) for t in twl]
    #     csvlist.append(tmplist)
    # with open('aa/sums.csv', 'wb') as fd:
    #     writer = csv.writer(fd, lineterminator='\n')
    #     writer.writerows(csvlist)


if __name__ == "__main__":
    main()
