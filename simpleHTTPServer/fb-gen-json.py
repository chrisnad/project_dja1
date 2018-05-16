#!/usr/bin/env python

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as pt
import networkx as nx
import json
import urllib2
from networkx.readwrite import json_graph
import math
import random
import namesgenerator



def genpoint(lon, lat, r):
    # Radius in Km 
    # generate points
    circlePoint = []
    #N is 1 degree:
    N = random.randint(0,360)
    angle = math.pi*2*N/360
    dx = random.uniform(0,r)*math.cos(angle)
    dy = random.uniform(0,r)*math.sin(angle)
    point = {}
    point['lat']= lat + (180/math.pi)*(dy/6371) #Earth Radius
    point['lon']= lon + (180/math.pi)*(dx/6371)/math.cos(lon*math.pi/180) #Earth Radius
    # add to list
    circlePoint.append(point)
    return point



mapbox_access_token = 'pk.eyJ1IjoiY2xlaXR1cyIsImEiOiJjamgwZ2c1a3Yxc3dtMnFtb2ptdDR5ZWs0In0.sjZdn45v32AojmWGWIN9Tg'
pt.set_credentials_file(username='cleitus', api_key='LN8W33LMo7kMNz2LU7Ce')



# ########################### Retrieving Data ###################################



G=nx.Graph()
gi=nx.Graph()

fileNums=[3980, 686, 414, 348, 0]
group_center=[[48.891986,2.319287],[48.878562,2.360369],[48.843491,2.351834],[48.858370,2.294481],[48.864049,2.331053]]
g = 0
for i in fileNums:
    fileName= "fb-edges/"+str(i)+".edges"
    gi = nx.read_edgelist(fileName, nodetype=int)
    for j in gi.nodes():
        gi.add_node(j, group = g)
        gi.add_node(j, name = namesgenerator.get_random_name())
        gi.add_node(j, istrain = bool(random.getrandbits(1)))
        cen_lat=group_center[g][0]
        cen_lon=group_center[g][1]
        point = genpoint(cen_lon, cen_lat, 0.5*len(gi.nodes())/60)
        gi.add_node(j, lat = point['lat'])
        gi.add_node(j, lon = point['lon'])
        gi.add_node(j, id = int(j))
    g+=1
    G = nx.compose(G,gi)

M = G


# ########################### Retrieving Data ###################################



#Write out initial graph data in JSON files
jsonData = json_graph.node_link_data(M)
with open('fb_nodes.json', 'w') as outfile:  
    json.dump(jsonData['nodes'], outfile, indent=4)

with open('fb_edges.json', 'w') as outfile:  
    json.dump(jsonData['links'], outfile, indent=4)