#!/usr/bin python
# -*- coding: utf-8 -*-

from pylab import *
import networkx as nx
import dircache
import json


def main():
    me = "wata88"
    user = {}
    user[me] = []
    for u in dircache.listdir('tmp/'):
        if u != '.DS_Store':
            user[me].append(u)
            try:
                jo = json.load(open('tmp/' + u + '/favorites.json', 'rb'))
            except:
                continue
            user[u] = []
            for fav in jo['favorites']:
                if fav['name']:
                    user[u].append(fav['name'])

    G = nx.Graph()
    for u in user[me]:
        G.add_edge(me, u)
    
    for u in user[me]:
        try:
            for f in user[u]:
                if f in user[me]:
                    G.add_edge(u, f)
        except:
            pass

    pos = nx.spring_layout(G)

    nx.draw_networkx_nodes(G, pos, node_size=50, node_color='w')
    nx.draw_networkx_edges(G, pos, width=1)
    nx.draw_networkx_labels(G, pos, font_size=12,
        font_family = 'sans-serif', font_color = 'b')

    nx.draw_networkx_nodes(G, pos, nodelist=[me], node_size=100, node_color='r')

    xticks([])
    yticks([])
    savefig("network.png")
    show()

if __name__ == "__main__":
    main()
