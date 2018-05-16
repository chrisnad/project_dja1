import networkx as nx
#import pandas as pd
#import numpy as np

#g = nx.read_edgelist('edgelist.txt')
#print(nx.info(g))

# show all data, including weights and attributes
#g.nodes(data=True)
#g.edges(data=True)

# number of edges / nodes
#len(g) # or g.number_of_nodes()
#g.number_of_edges()

# number connections for each node
#g.degree()

#Sorting a list of nodes based on their degree (this is how you sort dict by value)
#import operator
#sorted_g = sorted(g.degree().items(), key=operator.itemgetter(1), reverse=True)

#Adjacency Matrix
#mat = nx.to_pandas_adjacency(g)

#Adjacency matrix can also be loaded back to a graph
#G = nx.Graph(mat)
#print(nx.info(G))



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

#print "list of nodes: "
#print M.nodes(data = True)
#print "list of edges: "
#print M.edges(data = True)


#Eigenvector centrality criteria
Meigen=nx.eigenvector_centrality(M)
normeigen = [float(i)/max(Meigen.values()) for i in Meigen.values()]


#Closeness centrality
Mclose=nx.closeness_centrality(M)
normclose = Mclose.values()


#Betweeness centrality
Mbetween=nx.betweenness_centrality(M)
normbetween = Mbetween.values()


#Graph edges in list form
Medges = [i for i in M.edges()]


#Layout
pos=nx.fruchterman_reingold_layout(M, dim=3)
N=len(M.nodes())
labels=[i[1]['name'] for i in M.nodes(data = True)]


#Nodes and Edges coordinates
Xv=[pos[k][0] for k in range(N)]
Yv=[pos[k][1] for k in range(N)]
Zv=[pos[k][2] for k in range(N)]
Xed=[]
Yed=[]
Zed=[]
for edge in M.edges():
    Xed+=[pos[edge[0]][0],pos[edge[1]][0], None]
    Yed+=[pos[edge[0]][1],pos[edge[1]][1], None]
    Zed+=[pos[edge[0]][2],pos[edge[1]][2], None]


#Plotly
import plotly.plotly as py
from plotly.graph_objs import *

trace1=Scatter3d(x=Xed,
               y=Yed,
               z=Zed,
               mode='lines',
               line=Line(color='rgb(125,125,125)', width=1),
               hoverinfo='none'
               )

trace2=Scatter3d(x=Xv,
               y=Yv,
               z=Zv,
               mode='markers',
               name='actors',
               marker=Marker(symbol='dot',
                             color=normeigen, #
							 #color=normbetween, #
							 #color=normclose, #
                             #color=[data['nodes'][k]['group'] for k in range(len(data['nodes']))], #

                             size=6,colorbar=ColorBar(
                title=''
            ),
                             colorscale='Viridis',
                             line=Line(color='rgb(158,18,130)', width=0.5)
                             ),
               text=labels,
               hoverinfo='text'
               )

data=Data([trace1, trace2])
py.plot(data, filename = 'miserables_nx-2d')