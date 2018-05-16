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

def function():
	cen_lat=48.856813
	cen_lon=2.346654



	mapbox_access_token = 'pk.eyJ1IjoiY2xlaXR1cyIsImEiOiJjamgwZ2c1a3Yxc3dtMnFtb2ptdDR5ZWs0In0.sjZdn45v32AojmWGWIN9Tg'
	pt.set_credentials_file(username='cleitus', api_key='LN8W33LMo7kMNz2LU7Ce')



	# ########################### Retrieving Data ###################################



	data = []
	req = urllib2.Request("https://raw.githubusercontent.com/plotly/datasets/master/miserables.json")
	opener = urllib2.build_opener()
	f = opener.open(req)
	data = json.loads(f.read())  #data is a dict



	# ########################### Retrieving Data ###################################



	nodes = data[data.keys()[0]]
	links = data[data.keys()[1]]

	M = nx.Graph()

	M = nx.Graph([(i['source'], i['target'], {'value' : i['value']}) for i in links])

	for i in M.nodes():
		M.add_node(i, group = nodes[i]['group'])
		M.add_node(i, name = nodes[i]['name'])
		M.add_node(i, istrain = bool(random.getrandbits(1)))
		point = genpoint(cen_lon, cen_lat, 1)
		M.add_node(i, lat = point['lat'])
		M.add_node(i, lon = point['lon'])



	#Write out initial graph data in JSON file
	jsonData = json_graph.node_link_data(M)
	with open('evo_0.json', 'w') as outfile:  
		json.dump(jsonData, outfile, indent=4)



	#Eigenvector centrality criteria
	Meigen=nx.eigenvector_centrality(M)
	normeigen = [float(i)/max(Meigen.values()) for i in Meigen.values()]


	#Closeness centrality
	Mclose=nx.closeness_centrality(M)
	normclose = Mclose.values()


	#Betweeness centrality
	Mbetween=nx.betweenness_centrality(M)
	normbetween = Mbetween.values()


	N=len(M.nodes())
	labels=[i[1]['name'] for i in M.nodes(data = True)]



	# ###################### Evolution ####################



	import operator

	# Common Neighbors
	CN = [(e[0], e[1], len(list(nx.common_neighbors(M, e[0], e[1])))) for e in nx.non_edges(M)]
	CN.sort(key=operator.itemgetter(2), reverse = True)

	# Jaccard coef
	jaccard = list(nx.jaccard_coefficient(M))
	jaccard.sort(key=operator.itemgetter(2), reverse = True)

	# Resource Allocation index
	RA = list(nx.resource_allocation_index(M))
	RA.sort(key=operator.itemgetter(2), reverse = True)

	# Adamic-Adar index
	AA = list(nx.adamic_adar_index(M))
	AA.sort(key=operator.itemgetter(2), reverse = True)

	# Preferential Attachement
	PA = list(nx.preferential_attachment(M))
	PA.sort(key=operator.itemgetter(2), reverse = True)

	# Community Common Neighbors !!! requires graph to have node attribute: 'community' !!!
	#CCN = list(nx.cn_soundarajan_hopcroft(M))
	#CCN.sort(key=operator.itemgetter(2), reverse = True)

	# Community Resource Allocation !!! requires graph to have node attribute: 'community' !!!
	#CRA = list(nx.ra_index_soundarajan_hopcroft(M))
	#CRA.sort(key=operator.itemgetter(2), reverse = True)



	# ###################### Prediction on Future Edge Linkage ####################



	FM = M
	for i in PA[0:int(0.1*len(M.edges()))]:
		FM.add_edge(i[0], i[1], value='new')

	for i in CN[0:int(0.1*len(M.edges()))]:
		FM.add_edge(i[0], i[1], value='new')



	#Write out evolved graph data in JSON file
	jsonData = json_graph.node_link_data(FM)
	with open('evo_1.json', 'w') as outfile:  
		json.dump(jsonData, outfile, indent=4)

	return