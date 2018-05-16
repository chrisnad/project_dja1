#!/usr/bin/env python

import plotly.plotly as py
from plotly.graph_objs import *
import plotly.tools as pt
import networkx as nx
import json
import urllib2
from networkx.readwrite import json_graph
import math
import random
import operator


def function():
    mapbox_access_token = 'pk.eyJ1IjoiY2xlaXR1cyIsImEiOiJjamgwZ2c1a3Yxc3dtMnFtb2ptdDR5ZWs0In0.sjZdn45v32AojmWGWIN9Tg'
    pt.set_credentials_file(username='zhening', api_key='9LICBZ681YiPTiSZCuFX')

    # ########################### Reading Initial Data ###################################
    with open('fb_nodes.json') as f:
        nodes = json.load(f)

    with open('fb_edges.json') as f:
        links = json.load(f)

    for i in links:
        i['value'] = 'init'

    # ########################### Reading Initial Data ###################################

    #nodes = data['nodes']
    #links = data['edges']

    M = nx.Graph()

    M = nx.Graph(
        [(i['source'], i['target'], {'value': i['value']}) for i in links])
    for i in range(len(M.nodes)):
        node = nodes[i]['id']
        M.add_node(node, group=nodes[i]['group'])
        M.add_node(node, name=nodes[i]['name'])
        M.add_node(node, istrain=nodes[i]['istrain'])
        M.add_node(node, lat=nodes[i]['lat'])
        M.add_node(node, lon=nodes[i]['lon'])
        M.add_node(node, id=nodes[i]['id'])


    # ###################### Evolution ####################


    # Common Neighbors
    CN = [(e[0], e[1], len(list(nx.common_neighbors(M, e[0], e[1]))))
          for e in nx.non_edges(M)]
    CN.sort(key=operator.itemgetter(2), reverse=True)

    # Jaccard coef
    jaccard = list(nx.jaccard_coefficient(M))
    jaccard.sort(key=operator.itemgetter(2), reverse=True)

    # Resource Allocation index
    RA = list(nx.resource_allocation_index(M))
    RA.sort(key=operator.itemgetter(2), reverse=True)

    # Adamic-Adar index
    AA = list(nx.adamic_adar_index(M))
    AA.sort(key=operator.itemgetter(2), reverse=True)

    # Preferential Attachement
    PA = list(nx.preferential_attachment(M))
    PA.sort(key=operator.itemgetter(2), reverse=True)

    # ###################### Prediction on Future Edge Linkage ####################

    FM = M
    for i in PA[0:int(0.1*len(M.edges()))]:
        FM.add_edge(i[0], i[1], value='new')

    for i in CN[0:int(0.1*len(M.edges()))]:
        FM.add_edge(i[0], i[1], value='new')

    #Layout
    pos=nx.fruchterman_reingold_layout(FM, dim=3)
    lay=list()
    for i in pos.values():
        lay.append(list(i))
    N = len(FM.nodes())
    
    ulti = {}
    for i in pos.keys():
        ulti[i]=list(pos[i])

    #Eigenvector centrality criteria (normalised)
    Geigen=nx.eigenvector_centrality(FM)
    for i in Geigen:
        ulti[i].append(float(Geigen[i])/max(Geigen.values()))

    #Closeness centrality
    Gclose=nx.closeness_centrality(FM)
    for i in Gclose:
        ulti[i].append(Gclose[i])

    #Betweeness centrality
    Gbetween=nx.betweenness_centrality(FM)
    for i in Gbetween:
        ulti[i].append(Gbetween[i])

    # ###################### Plot ####################

    # Nodes and Edges coordinates
    Xv=[lay[k][0] for k in range(N)]# x-coordinates of nodes
    Yv=[lay[k][1] for k in range(N)]# y-coordinates
    Zv=[lay[k][2] for k in range(N)]# z-coordinates
    Xed = []
    Yed = []
    Zed = []
    Xned = []
    Yned = []
    Zned = []
    for edge in M.edges():
        Xed+=[pos[edge[0]][0],pos[edge[1]][0], None]
        Yed+=[pos[edge[0]][1],pos[edge[1]][1], None]
        Zed+=[pos[edge[0]][2],pos[edge[1]][2], None]

    for edge in [(i[0], i[1]) for i in list(FM.edges(data=True)) if i[2]['value'] == 'new']:
        Xned+=[pos[edge[0]][0],pos[edge[1]][0], None]
        Yned+=[pos[edge[0]][1],pos[edge[1]][1], None]
        Zned+=[pos[edge[0]][2],pos[edge[1]][2], None]


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
    py.plot(data, filename = 'fb-3d')
    return
