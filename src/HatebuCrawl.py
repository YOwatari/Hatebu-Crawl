#!/usr/bin python
# -*- coding: utf-8 -*-

import json
import os
import sys
import requests


class HatebuCrawl(object):
    def __init__(self, user):
        self.__current = user
        self.setUser()
        self.count = 0
        self.favJson = None

    def setUser(self):
        # ユーザー関連情報をセットする
        self.__dirs = "tmp/" + self.__current + "/"
        self.__filepath = self.__dirs + "favorites.json"
        self.__favorites_url = "http://www.hatena.ne.jp/" + \
            self.__current + "/favorites.json"

    def getFavorites(self):
        # お気に入りユーザを取得する
        if self.favJson is None:
            if os.path.exists(self.__filepath):
                self.favJson = json.load(open(self.__filepath, 'rb'))
            else:
                try:
                    r = requests.get(self.__favorites_url)
                except requests.exceptions.RequestException as e:
                    return e
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
