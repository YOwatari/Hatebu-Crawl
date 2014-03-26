#!/usr/bin python
# -*- coding: utf-8 -*-

import json
import os
import requests


class HatebuCrawl(object):
    def __init__(self, user):
        self.__current = user
        self.setUser()
        self.favJson = None
        self.Feed = None
        self.NextFeed = False

    def setUser(self):
        # ユーザー関連情報をセットする
        self.__dirs = "tmp/" + self.__current + "/"
        self.__filepath = self.__dirs + "favorites.json"
        self.__favorites_url = "http://www.hatena.ne.jp/" + \
            self.__current + "/favorites.json"
        self.bookmarks_url = "http://b.hatena.ne.jp/" + \
            self.__current + "/atomfeed"

    def getFavorites(self):
        # お気に入りユーザを取得する
        if self.favJson is None:
            if os.path.exists(self.__filepath):
                self.favJson = json.load(open(self.__filepath, 'rb'))
            else:
                try:
                    r = requests.get(self.__favorites_url)
                except requests.exceptions.RequestException as e:
                    return str(e)
                self.favJson = r.json()
        return json.dumps(self.favJson, sort_keys=True, indent=4)

    def saveFavorites(self):
        # お気に入りユーザをファイルに保存する
        if self.favJson is None:
            self.getFavorites()
        if not os.path.exists(self.__dirs):
            os.makedirs(self.__dirs)
        json.dump(self.favJson, open(self.__filepath, 'wb'),
                  sort_keys=True, indent=4)
        return "Favorites json file saved."

    def getBookmarks(self, date):
        # 指定日時のブックマークを得る
        try:
            r = requests.get(self.bookmarks_url, params={'date': date})
        except requests.exceptions.RequestException as e:
            return str(e)
        self.Feed = r
        return self.Feed.text

    def saveBookmarks(self, date):
        # 指定日時のブックマークをファイルに保存する
        _ = self.getBookmarks(date)

        with open(self.__dirs + "/" + date + ".xml", 'wb') as fd:
            for chunk in self.Feed.iter_content(100):
                fd.write(chunk)
        return "Bookmarks feed file saved."
