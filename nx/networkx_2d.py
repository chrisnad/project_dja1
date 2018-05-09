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
 
G=nx.Graph()
gi=nx.Graph()

fileNums=[0]
for i in fileNums:
    fileName="../Datasets/facebook/edges/"+str(i)+".edges"
    gi = nx.read_edgelist(fileName)
    G = nx.compose(G,gi)

print(nx.info(G))

#Layout
pos=nx.fruchterman_reingold_layout(G, dim=3)
lay=list()
for i in pos.values():
    lay.append(list(i))

N=len(G.nodes())
#labels=[i for i in pos.keys()]

ulti = {}
for i in pos.keys():
    ulti[i]=list(pos[i])

#Eigenvector centrality criteria (normalised)
Geigen=nx.eigenvector_centrality(G)
for i in Geigen:
    ulti[i].append(float(Geigen[i])/max(Geigen.values()))

#Closeness centrality
Gclose=nx.closeness_centrality(G)
for i in Gclose:
    ulti[i].append(Gclose[i])

#Betweeness centrality
Gbetween=nx.betweenness_centrality(G)
for i in Gbetween:
    ulti[i].append(Gbetween[i])


#Nodes and Edges coordinates
Xv=[k[0] for k in pos.values()]
Yv=[k[1] for k in pos.values()]
Xed=[]
Yed=[]
for edge in G.edges():
    Xed+=[pos[edge[0]][0],pos[edge[1]][0], None]
    Yed+=[pos[edge[0]][1],pos[edge[1]][1], None]


#Plotly
import plotly.plotly as py
from plotly.graph_objs import *

trace1=Scatter(x=Xed,
               y=Yed,
               mode='lines',
               line=Line(color='rgb(125,125,125)', width=1),
               hoverinfo='none'
               )

trace2=Scatter(x=Xv,
               y=Yv,
               mode='markers',
               name='actors',
               marker=Marker(symbol='dot',
                             color=[i[-3] for i in ulti.values()], # Eigenvector centrality
							 #color=[i[-2] for i in ulti.values()], # Closeness centrality
							 #color=[i[-1] for i in ulti.values()], # Betweeness centrality
                             #color=[data['nodes'][k]['group'] for k in range(len(data['nodes']))], #

                             size=6,colorbar=ColorBar(
                title=''
            ),
                             colorscale='Viridis',
                             line=Line(color='rgb(158,18,130)', width=0.5)
                             ),
               text=ulti.keys(),  # node Labels
               hoverinfo='text'
               )

data=Data([trace1, trace2])
py.plot(data, filename = 'networkx-2d')