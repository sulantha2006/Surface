__author__ = 'sulantha'
from scipy import cluster
import numpy as np
import networkx as nx
from tvtk.api import tvtk
from mayavi import mlab
from mayavi.mlab import *
import os


def setSysPaths():
    templateFileFullPath = ''
    templateFileDir =''


def readTemplateFile(templateFile):
    with open(templateFile) as f:
        lines = f.read().splitlines()
    pointsList = [map(float, x.split(' ')) for x in lines[1:int(lines[0])+1]]
    triangleList = [[int(k)-1 for k in y.split(' ')] for y in lines[int(lines[0])+2:len(lines)]]
    return pointsList, triangleList


def performClustering(pointsList, numberOfClusters):
    centroids, labels = cluster.vq.kmeans2(np.array(pointsList), numberOfClusters, iter=5, minit='points')
    return centroids, labels


def generateConnectomeGraph(numberOfNodes, connectivityCSV, threshold):
    G = nx.Graph()
    G.add_nodes_from(range(numberOfNodes))

    f = open(connectivityCSV)
    nodeSize = []
    for i in range(numberOfNodes):
        node_i_size = 1
        line = f.readline()
        connectivityValues = str(line).strip().split(',')
        for k in range(len(connectivityValues)):
            if float(connectivityValues[k]) > threshold:
                node_i_size = node_i_size + 1
                l = []
                tupel_t = (i, k, {'weight': float(connectivityValues[k])})
                l.append(tupel_t)
                G.add_edges_from(l)
        nodeSize.append(node_i_size)
    f.close()
    return G, nodeSize


def draw3dDPlot(pointsOnGraph, graph, nodeSize):
    p_x = zip(*pointsOnGraph)[0]
    p_y = zip(*pointsOnGraph)[1]
    p_z = zip(*pointsOnGraph)[2]
    edge_size = 0.1
    node_scale = 0.1
    graph_colormap ='winter'
    pnts = mlab.points3d(np.array(p_x), np.array(p_y), np.array(p_z), nodeSize, scale_factor=node_scale, colormap=graph_colormap)
    pnts.mlab_source.dataset.lines = np.array(graph.edges())
    tube = mlab.pipeline.tube(pnts, tube_radius=edge_size)
    mlab.pipeline.surface(tube)


def polydata(pointsList, triangleList):
    points = np.array(pointsList, 'f')
    triangles = np.array(triangleList)
    scalars = [int(str(value).strip()) for value in open('Data/ad_summary_connectivity.csv').readlines()]

    # The TVTK dataset.
    mesh = tvtk.PolyData(points=points, polys=triangles)
    mesh.point_data.scalars = scalars
    mesh.point_data.scalars.name = 'scalars'
    return mesh


def view(dataset):
    fig = mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), figure=dataset.class_name[3:])
    surf = mlab.pipeline.surface(dataset, opacity=0.5)
    #mlab.pipeline.surface(mlab.pipeline.extract_edges(surf), color=(0, 0, 0), )


pointsList, triangleList = readTemplateFile('Templates/BrainMesh_ICBM152_smoothed.nv')
centroids, labels = performClustering(pointsList, 2000)
graph, nodeSize = generateConnectomeGraph(2000, 'Data/ad_connectivity.csv', 0.8)
view(polydata(pointsList, triangleList))
draw3dDPlot(centroids, graph, nodeSize)

mlab.show()