#!/usr/bin python
# -*- coding: utf-8 -*-

import twitter

import re
import csv
import time

myapp_apikeys = {
    "cons_key": "cNTevc2CXDVOs59WJB98Fg",
    "cons_sec": "8rV37QS0YkNGpFID2KEOuDseeHgsbQuR9UffFldA",
    "token_key": "13154302-XEOoyWXrEVtfmKnuqW3ZZFqcJLjkfyON2VrxUGjiY",
    "token_sec": "j8viLyze43pUceIDmV588vUkMZBwhljK0mec8lKfhkld5"
}

patrn1 = re.compile(r"(\[.*\]|\(.*\)|【.*】|<.*>|（.*）|〔.*〕)")
patrn2 = re.compile(r"(DVD|Blu-ray|ブルーレイ|枚組).*")
patrn3 = re.compile(r"\s.*(MovieNEX|2D|3D|エディション|ディスク|特別(編|版)).*")
patrn4 = re.compile(r"\s$")


class TwitterCrawler(object):
    def __init__(self, apikeys):
        self._lang = 'ja'
        self._api = twitter.Api(
            consumer_key=apikeys['cons_key'],
            consumer_secret=apikeys['cons_sec'],
            access_token_key=apikeys['token_key'],
            access_token_secret=apikeys['token_sec'],
            cache=None)

    def search(self, query):
        tweets = self._api.GetSearch(
            term=query,
            lang=self._lang,
            result_type="recent")
        return tweets


def normalize_list():
    inlist = []
    outlist = []
    with open('AmazonRecommendMovies.csv', 'rb') as fd:
        reader = csv.reader(fd)
        for row in reader:
            inlist = inlist + row
    for r in inlist:
        m = patrn1.sub("", r)
        m = patrn2.sub("", m)
        m = patrn3.sub("", m)
        m = patrn4.sub("", m)
        outlist.append(m)
    outlist = list(set(outlist))
    with open('movielist.txt', 'wb') as fd:
        for r in outlist:
            fd.write(r+"\n")


def inputlist():
    tmp = []
    with open('mm.txt', 'rb') as fd:
        for line in fd:
            tmp.append(line)
    tmp = list(set(tmp))
    with open('mm.txt', 'wb') as fd:
        for r in tmp:
            fd.write(r)


def GetTweets():
    movies = []
    with open('movielist.txt', 'rb') as fd:
        for line in fd:
            movies.append(line)
    movies = list(set(movies))

    tw = TwitterCrawler(myapp_apikeys)

    outcsv = []
    users = []
    for i in xrange(0, len(movies)):
        tmp = []
        for j in xrange(0, len(movies)):
            print i, j
            if i == j:
                tmp.append(0)
                query = movies[i]
                try:
                    tweets = tw.search(movies[i].decode('utf-8'))
                    if len(tweets) > 0:
                        with open('tw/'+str(i)+'.txt', 'wb') as fd:
                            for tweet in tweets:
                                fd.write(str(tweet.user.id) + "," + tweet.text.encode('utf-8') + "\n")
                                users.append(tweet.user.id)
                    time.sleep(5)
                except Exception as e:
                    print str(e)
                    continue
            elif j < i:
                tmp.append(0)
            else:
                query = movies[i]+" "+movies[j]
                try:
                    tweets = tw.search(query.decode('utf-8'))
                    if len(tweets) > 0:
                        with open('tw/'+str(i)+"_"+str(j)+'.txt', 'wb') as fd:
                            for tweet in tweets:
                                fd.write(str(tweet.user.id) + "," + tweet.text.encode('utf-8') + "\n")
                                users.append(tweet.user.id)
                    tmp.append(len(tweets))
                    time.sleep(5)
                except Exception as e:
                    print str(e)
                    continue
        outcsv.append(tmp)

    with open('tw/sums.csv', 'wb') as fd:
        writer = csv.writer(fd, lineterminator='\n')
        writer.writerows(outcsv)

    users = list(set(users))
    with open('tw/users.txt', 'wb') as fd:
        for user in users:
            fd.write(str(user) + "\n")


if __name__ == "__main__":
    GetTweets()
