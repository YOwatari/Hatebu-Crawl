#!/usr/bin python
# -*- coding: utf-8 -*-

import twitter_keys

import twitter

import csv
import time


class TwitterCrawler(object):
    def __init__(self):
        self._lang = 'ja'
        self._api = twitter.Api(
            consumer_key=twitter_keys.apikeys['cons_key'],
            consumer_secret=twitter_keys.apikeys['cons_sec'],
            access_token_key=twitter_keys.apikeys['token_key'],
            access_token_secret=twitter_keys.apikeys['token_sec'],
            cache=None)
        self.users = []
        self.matrix = []

    def search(self, query):
        tweets = self._api.GetSearch(
            term=query,
            lang=self._lang,
            result_type="recent")
        return tweets

    def save_tweets(self, filename, tweets):
        with open('tw/' + filename + '.txt', 'wb') as fd:
            for tweet in tweets:
                fd.write(
                    str(tweet.id) + ","
                    + str(tweet.user.id) + ","
                    + tweet.text.encode('utf-8') + "\n"
                )
                self.users.append(tweet.user.id)

    def get_tweets(self, movies):
        for i in xrange(len(movies)):
            sums = []
            for j in xrange(len(movies)):
                if i == j:
                    sums.append(0)
                    # query = movies[i].decode('utf-8')
                    # try:
                    #     tweets = self.search(query)
                    #     if len(tweets) > 0:
                    #         self.save_tweets(query, tweets)
                    #     time.sleep(5)
                    # except Exception as e:
                    #     print str(e)
                    #     continue
                elif j < i:
                    sums.append(0)
                else:
                    query = movies[i]+" "+movies[j]
                    query = query.decode('utf-8')
                    try:
                        tweets = self.search(query)
                        if len(tweets) > 0:
                            self.save_tweets(query, tweets)
                        sums.append(len(tweets))
                        time.sleep(5)
                    except Exception as e:
                        print str(e)
                        continue
            self.matrix.append(sums)

    def save_matrix(self, path="sums.csv"):
        with open('tw/' + path, 'wb') as fd:
            writer = csv.writer(fd, lineterminator='\n')
            writer.writerows(self.matrix)

    def save_users(self, path="users.txt"):
        users = list(set(self.users))
        with open('tw/' + path, 'wb') as fd:
            for user in users:
                fd.write(str(user) + "\n")
