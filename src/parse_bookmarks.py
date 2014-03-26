#!/usr/bin python
# -*- coding: utf-8 -*-

import feedparser
import dircache
import re
import csv
import sys

def FeedParse():
    c = 0
    # ファイルからそれぞれの要素を取得
    rows = []
    patern = re.compile(r'\d*\.xml$')
    for u in dircache.listdir('tmp/'):
        if u == '.DS_Store':
            continue
        index = 0
        for f in dircache.listdir('tmp/' + u):
            if patern.search(f) is not None:
                d = feedparser.parse('tmp/' + u + '/' + f)
                if d['entries'] == []:
                    continue
                for e in d['entries']:
                    tags = ""
                    try:
                        tags = [t['term'] for t in e['tags']]
                        tags = ",".join(tags)
                    except:
                        pass
                    try:
                        rows.append({
                            "user": e['author'].encode('utf-8'),
                            "id": str(index).encode('utf-8'),
                            "title": e['title'].encode('utf-8'),
                            "url": e['links'][0]['href'].encode('utf-8'),
                            "summary": e['summary'].encode('utf-8'),
                            "tags": tags.encode('utf-8'),
                            "date": e['published'].encode('utf-8'), })
                        index += 1
                    except Exception as err:
                        print str(err)
                        pass
                    c += 1
                    sys.stdout.write("\r%d" % c)
    print "\n"
    params = ["user", "id", "url", "date", "tags", "summary", "title"]
    header = dict([(v, v) for v in params])
    rows.insert(0, header)
    with open('bookmarks.csv', 'wb') as fd:
        #writer = csv.DictWriter(fd, params, extrasaction='ignore')
        #writer.writerows(rows)
        for row in rows:
            tmplist = []
            for p in params:
                tmplist.append(row[p])
            tmp = ''
            for w in tmplist:
                tmp = tmp + '\"' + w + '\"\t'
            fd.write(tmp[:-1] + '\n')


if __name__ == "__main__":
    FeedParse()
