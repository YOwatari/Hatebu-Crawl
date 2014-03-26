#!/usr/bin python
# -*- coding: utf-8 -*-

from AcademyAward import AcademyAward as aa
from AmazonMovies import AmazonMovies as am
from TwitterCrawler import TwitterCrawler as tc

import numpy as np
import csv

academy = aa(2010)
aa.save_movies()

amazon = am(academy.movies)
amazon.save_movies()

twitter = tc()
movies = academy.movies + amazon.movies
twitter.search(movies)

matrix = []


def normalize(matrix):
    tmp_rows = 0
    for line in matrix:
        tmp_sums = 0
        for item in line:
            tmp_sums = tmp_sums + int(item)
        tmp_line = []
        for item in line:
            try:
                tmp_line.append(float(item)/float(tmp_sums))
            except ZeroDivisionError:
                tmp_line.append(0.0)
        tmp_rows.append(tmp_line)

    with open('tw/sums_normalize.csv', 'wb') as fd:
        writer = csv.writer(fd, lineterminator='\n')
        writer.writerows(tmp_rows)

    return tmp_rows


def sums_tweets():
    sums = 0
    with open('tw/sums.csv', 'rb') as fd:
        for line in fd:
            row = line.split(',')
            for i in row:
                sums = sums + int(i)
    print sums


def sim_cos(target):
    array = np.array(matrix)

    tmp_dict = []
    for i in xrange(len(array)):
        if i == target:
            continue
        try:
            a = np.dot(array[target], array[i])
            b = np.linalg.norm(array[target])*np.linalg.norm(array[i])
            if a != 0 and b != 0:
                tmp_dict[i] = a/b
        except ValueError:
            tmp_dict[i] = 0.0

    output = []
    for k, v in sorted(tmp_dict.items(), key=lambda x:x[1], reverse=True):
        if movies[k][:-1].decode('utf-8') != u"天使の分け前":
            output.append({
                'title': movies[k][:-1],
                'value': v
            })
    return output[0:10]


if __name__ == "__main__":
    matrix = normalize(twitter.matrix)
    # query2010 = [52, 83, 184, 132, 203, 76, 15, 141, 90, 111]
    # query2011 = [38, 102, 51, 43, 98, 23, 192, 91, 32]
    # query2012 = [151, 164, 155, 7, 79, 140, 127, 122]
    # query2013 = [195, 27, 154, 117, 42, 82, 146, 0, 105]
    movies_dict = []
    for i, movie in enumerate(academy.movies):
        movies_dict.append({
            'title': movie,
            'relations': sim_cos(i),
            'similars': amazon.movies_dict[i]['similars']
        })

    outrows = []
    for movie in movies_dict:
        tmpline = []
        for i in movie['relations']:
            tmpline.append({
                'title': movies['title'],
                'rank': i,
                'relations': movie['relations'][i],
                'similars': movie['similars'][i]
            })
        outrows.append(tmpline)

    params = ['title', 'rank', 'relations', 'similars']
    header = dict([(v, v) for v in params])
    outrows.insert(0, header)
    with open('OUTPUT.csv', 'wb') as fd:
        writer = csv.DictWriter(fd, params, extrasaction='ignore')
        writer.writerows(outrows)
