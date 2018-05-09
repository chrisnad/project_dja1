from igraph import * 
G=Graph()

def addVertex(g,name_str):
    try:
        if(name_str not in g.vs['name']):
            #print('Inserted node ',name_str)
            g.add_vertex(name=name_str)
        #else:
            #print ('Node ',name_str,' already present')
            #print(g.vs.find(name_str).index)   
    except KeyError:
        g.add_vertex(name=name_str)
    return g

def write_tuple_to_file(f,t):
    string=str(t[0])+' '+str(t[1])+'\n'
    f.write(string)

def retrieve_edge_name_tuple(g,t):
    a=(g.vs[t[0]]['name'],g.vs[t[1]]['name'])
    return a


def load_dataset(fileName,g):
    fileNums=[0]
    for i,eachNum in enumerate(fileNums):
        #print(eachNum)
        fileName="../Datasets/facebook/edges/"+str(eachNum)+".edges"
        #print('fileName=',fileName)
        f=open(fileName)
        line=f.readline()
        while(line!=''):
            c=(line.split())
            g=addVertex(g,c[0])
            g=addVertex(g,c[1])
            #print('Adding ',c[0],'-->',c[1])
            g.add_edge(c[0],c[1]) 
            line=f.readline()
    g.simplify()    
    return

load_dataset('abd',G)

def calculate_eigen(g):
    eigen=g.evcent(directed=False)
    for i in range(1,6):
        maxVal=max(eigen)
        print(i,'==node',g.vs[eigen.index(maxVal)]['name'],' with score of ',maxVal)
        eigen.remove(maxVal)
    eigen=g.evcent(directed=False)
    return eigen
	
def calculate_closeness(g):
    close=g.closeness(g.vs)
    for i in range(1,6):
        maxVal=max(close)
        print(i,'==node',g.vs[close.index(maxVal)]['name'],' with score of ',maxVal)
        close.remove(maxVal)
    close=g.closeness(g.vs)
    return close
	
def calculate_between(g):
    between=g.betweenness(g.vs)
    for i in range(1,6):
        maxVal=max(between)
        print(i,'==node',g.vs[between.index(maxVal)]['name'],' with score of ',maxVal)
        between.remove(maxVal)
    between=g.betweenness(g.vs)
    return between
	
global eigen
global close
global between

print('Eigen Vector:')
eigen=calculate_eigen(G)
print('Closeness')
close=calculate_closeness(G)
print('Betweenness')
between=calculate_between(G)


N=len(G.vs)
layt=G.layout('kk', dim=3)

labels=[]
#print(type(labels))
for eachNde in G.vs:
    labels.append(eachNde['name'])

Edges=list()
for eachTuple in G.es:
    Edges.append(eachTuple.tuple)

Xn=[layt[k][0] for k in range(N)]# x-coordinates of nodes
Yn=[layt[k][1] for k in range(N)]# y-coordinates
Zn=[layt[k][2] for k in range(N)]# z-coordinates
Xe=[]
Ye=[]
Ze=[]

for e in Edges:
    Xe+=[layt[e[0]][0],layt[e[1]][0], None]# x-coordinates of edge ends
    Ye+=[layt[e[0]][1],layt[e[1]][1], None]
    Ze+=[layt[e[0]][2],layt[e[1]][2], None]

import plotly
plotly.tools.set_credentials_file(username='cleitus', api_key='LN8W33LMo7kMNz2LU7Ce')

import plotly.plotly as py
from plotly.graph_objs import *


trace1=Scatter3d(x=Xe,
               y=Ye,
               z=Ze,
               mode='lines',
               line=Line(color='rgb(125,125,125)', width=1),
               hoverinfo='none'
               )

trace2=Scatter3d(x=Xn,
               y=Yn,
               z=Zn,
               mode='markers',
               name='actors',
               marker=Marker(symbol='dot',
                             color=eigen, #
							 #color=between, #
							 #color=close, #
                             size=6,colorbar=ColorBar(
                title='Colorbar'
            ),
                             colorscale='Viridis',
                             line=Line(color='rgb(158,18,130)', width=0.5)
                             ),
               text=labels,
               hoverinfo='text'
               )

axis=dict(showbackground=False,
          showline=False,
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title=''
          )

layout = Layout(
         title="3D Visualization of the Facebook nodes",
         width=1000,
         height=1000,
         showlegend=False,
         scene=Scene(
         xaxis=XAxis(axis),
         yaxis=YAxis(axis),
         zaxis=ZAxis(axis),
        ),
     margin=Margin(
        t=100
    ),
    hovermode='closest',
    annotations=Annotations([
           Annotation(
           showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=0.1,
            xanchor='left',
            yanchor='bottom',
            font=Font(
            size=14
            )
            )
        ]),    )

data=Data([trace1, trace2])
fig=Figure(data=data, layout=layout)

#py.iplot(fig, filename = 'test')

py.plot(data, filename = 'igraph-3d')