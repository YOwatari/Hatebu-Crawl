#!/usr/bin python
# -*- coding: utf-8 -*-

import requests
from pyquery import PyQuery as pq
import re

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
    print len(aa.movielist)


if __name__ == "__main__":
    main()
