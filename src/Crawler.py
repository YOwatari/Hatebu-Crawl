#!/usr/bin python
# -*- coding: utf-8 -*-

from src.HatebuCrawl import HatebuCrawl

import json
import time
import sys

# 取得ユーザ
user = "wata88"


def favCrawl(fav):
    # カウンター
    fav_count = 0
    fav_users = 0
    favfav_count = 0
    favfav_users = 0
    all_count = 0

    # お気に入りのお気に入りまでクロール
    jo = json.loads(fav)
    fav_users = len(jo['favorites'])
    for fav in jo['favorites']:
        # お気に入りユーザがいたら
        if fav['name']:
            fav_count = fav_count + 1
            tmp = HatebuCrawl(fav['name'])
            time.sleep(0.05)
            try:
                favfavJO = json.loads(tmp.getFavorites())
            except Exception as e:
                sys.stdout.write(
                    "\r Fav(%d/%d): %s FavFav: None" %
                    (fav_count, fav_users, fav['name']))
                continue
            tmp.saveFavorites()
            favfav_users = len(favfavJO['favorites'])
            for favfav in favfavJO['favorites']:
                favfav_count = favfav_count + 1
                if favfav['name']:
                    sys.stdout.write(
                        "\r Fav(%d/%d): %s FavFav(%d/%d): %s" %
                        (fav_count, fav_users, fav['name'],
                            favfav_count, favfav_users, favfav['name']))
        all_count = all_count + favfav_count
        favfav_count = 0
    # 最後に合計値を出力
    print "\n\nCrawled All Users: %d\n" % int(fav_users + all_count + 1)

if __name__ == "__main__":
    print "User: %s\n" % user

    h = HatebuCrawl(user)
    h.saveFavorites()
    favCrawl(h.getFavorites())
