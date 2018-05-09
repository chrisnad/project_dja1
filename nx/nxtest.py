import networkx as nx
import pandas as pd

g = nx.read_edgelist('edgelist.txt')
print(nx.info(g))

# show all data, including weights and attributes
g.nodes(data=True)
g.edges(data=True)

# number of edges / nodes
len(g) # or g.number_of_nodes()
g.number_of_edges()

# number connections for each node
g.degree()

#Sorting a list of nodes based on their degree
from operator import itemgetter
sorted(g.degree(), key=itemgetter(1), reverse=True)

#Adjacency Matrix
mat = nx.to_pandas_adjacency(g)

#Adjacency matrix can also be loaded back to a graph
G = nx.Graph(mat)
print(nx.info(G))



# miserables json graph
import json
import urllib2

data = []
req = urllib2.Request("https://raw.githubusercontent.com/plotly/datasets/master/miserables.json")
opener = urllib2.build_opener()
f = opener.open(req)
data = json.loads(f.read())  #data is a dict

nodes = data[data.keys()[0]]
links = data[data.keys()[1]]

M = nx.Graph()

M = nx.Graph([(i['source'], i['target'], {'value' : i['value']}) for i in links])
for i in M.nodes():
    M.add_node(i, group = nodes[i]['group'])
    M.add_node(i, name = nodes[i]['name'])

print "list of nodes: "
print M.nodes(data = True)
print "list of edges: "
print M.edges(data = True)