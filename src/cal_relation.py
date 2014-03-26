#!/usr/bin python
# -*- coding: utf-8 -*-

import numpy as np
import csv

rows = []
movies = []


def get_movies():
    with open('movielist.txt', 'rb') as fd:
        for line in fd:
            movies.append(line)


def normalize():
    with open('tw/sums.csv', 'rb') as fd:
        for line in fd:
            row = line.split(',')
            sums = 0
            for i in row:
                sums = sums + int(i)
            tmp = []
            for i in row:
                try:
                    tmp.append(float(i)/float(sums))
                except ZeroDivisionError:
                    tmp.append(0)
            rows.append(tmp)
    with open('sums_normalize.csv', 'wb') as fd:
        writer = csv.writer(fd, lineterminator='\n')
        writer.writerows(rows)


def sums_tweets():
    sums = 0
    with open('tw/sums.csv', 'rb') as fd:
        for line in fd:
            row = line.split(',')
            for i in row:
                sums = sums + int(i)
    print sums


def sim_cos(p1):
    array = np.array(rows)
    target_norm = np.linalg.norm(array[p1])

    tmplist = {}
    for i in xrange(0, len(array)):
        if i == p1:
            continue
        try:
            a = np.dot(array[p1], array[i])
            b = target_norm*np.linalg.norm(array[i])
            if a!=0 and b!=0:
                tmplist[i] = a/b
        except (ValueError):
            tmplist[i] = 0.0

    output_rows = []
    print "\nQuery: %s" % movies[p1][:-1]
    j = 0
    for k, v in sorted(tmplist.items(), key=lambda x:x[1], reverse=True):
        if j < 10:
            j = j + 1
            if movies[k][:-1].decode('utf-8') != u"天使の分け前":
                print "%s : %1.3f" % (movies[k][:-1], v)
                output_rows.append([movies[p1][:-1], movies[k][:-1], v])
    return output_rows


if __name__ == "__main__":
    normalize()
    get_movies()
    output = []
    query2010 = [52, 83, 184, 132, 203, 76, 15, 141, 90, 111]
    query2011 = [38, 102, 51, 43, 98, 23, 192, 91, 32]
    query2012 = [151, 164, 155, 7, 79, 140, 127, 122]
    query2013 = [195, 27, 154, 117, 42, 82, 146, 0, 105]
    for q in query2010+query2011+query2012+query2013:
        output = output + sim_cos(q)

    with open('OUTPUUUUUUUUT.csv', 'wb') as fd:
        writer = csv.writer(fd, lineterminator='\n')
        writer.writerows(output)
