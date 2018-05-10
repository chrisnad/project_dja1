import plotly.plotly as py
import plotly.graph_objs as go
import networkx as nx
import json
import urllib2
from networkx.readwrite import json_graph
import math
import random

cen_lat=48.856813
cen_lon=2.346654
lat_dist = 0.00900009

def lon_dist(lat):
    return 1/111.11/math.cos(lat)


mapbox_access_token = 'pk.eyJ1IjoiY2xlaXR1cyIsImEiOiJjamgwZ2c1a3Yxc3dtMnFtb2ptdDR5ZWs0In0.sjZdn45v32AojmWGWIN9Tg'

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
    M.add_node(i, istrain = bool(random.getrandbits(1)))
    M.add_node(i, lat = random.uniform(cen_lat - lat_dist, cen_lat + lat_dist))
    M.add_node(i, lon = random.uniform(cen_lon - lon_dist(cen_lat), cen_lon + lon_dist(cen_lat)))


#Write out graph data in JSON file
jsonData = json_graph.node_link_data(M)
with open('data/miserables.json', 'w') as outfile:  
    json.dump(jsonData, outfile, indent=4)

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
#Medges = [i for i in M.edges()]


#Layout
#pos=nx.fruchterman_reingold_layout(M, dim=2)
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




# ###################### Prediction on Node Attribute ####################



import pandas as pd

df = pd.DataFrame(index=M.nodes())

df['name'] = pd.Series(nx.get_node_attributes(M, 'name'))
df['group'] = pd.Series(nx.get_node_attributes(M, 'group'))
df['istrain'] = pd.Series(nx.get_node_attributes(M, 'istrain'))
df['lat'] = pd.Series(nx.get_node_attributes(M, 'lat'))
df['lon'] = pd.Series(nx.get_node_attributes(M, 'lon'))

df['eig'] = pd.Series(Meigen)
df['deg'] = pd.Series(nx.degree_centrality(M))
df['btw'] = pd.Series(Mbetween)
df['close'] = pd.Series(Mclose)
df['cluster'] = pd.Series(nx.clustering(M))



# ###################### Prediction on Future Edge Linkage ####################


FM = M
for i in PA[0:int(0.1*len(M.edges()))]:
    FM.add_edge(i[0], i[1], value='new')
for i in CN[0:int(0.1*len(M.edges()))]:
    FM.add_edge(i[0], i[1], value='new')



# ###################### Plot ####################



#Nodes and Edges coordinates
Xv=[M.nodes(data=True)[k]['lat'] for k in range(N)]
Yv=[M.nodes(data=True)[k]['lon'] for k in range(N)]
Xed=[]
Yed=[]
Xned=[]
Yned=[]
for edge in M.edges():
    Xed+=[M.nodes(data=True)[edge[0]]['lat'],M.nodes(data=True)[edge[1]]['lat'], None]
    Yed+=[M.nodes(data=True)[edge[0]]['lon'],M.nodes(data=True)[edge[1]]['lon'], None]

for edge in [(i[0], i[1]) for i in list(M.edges(data = True)) if i[2]['value'] == 'new']:
    Xned+=[M.nodes(data=True)[edge[0]]['lat'],M.nodes(data=True)[edge[1]]['lat'], None]
    Yned+=[M.nodes(data=True)[edge[0]]['lon'],M.nodes(data=True)[edge[1]]['lon'], None]

Meigen=nx.eigenvector_centrality(FM)
normeigen = [float(i)/max(Meigen.values()) for i in Meigen.values()]

data = [
    go.Scattermapbox(
        lat=Xed,
        lon=Yed,
        mode='lines',
        line=dict(color='rgb(125,125,125)', width=1),
        hoverinfo='none'
        ),
    go.Scattermapbox(
        lat=Xned,
        lon=Yned,
        mode='lines',
        line=dict(color='rgb(158,18,130)', width=1),
        hoverinfo='none'
        ),
    go.Scattermapbox(
        lat=Xv,
        lon=Yv,
        mode='markers',
        name='actors',
        marker=dict(size=10,
                    color=normeigen, #
				    #color=normbetween, #
					#color=normclose, #
                    #color=[data['nodes'][k]['group'] for k in range(len(data['nodes']))], #
                    #colorbar=dict(title=''),
                    colorscale='Viridis',
                    #line=dict(color='rgb(158,18,130)', width=0.5)
                    ),
        text=labels,
        hoverinfo='text'
        )
]

layout = go.Layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=48.856813,
            lon=2.346654
        ),
        pitch=0,
        zoom=12.50
    ),
)

fig = dict(data=data, layout=layout)
py.plot(fig, filename='Evolution')