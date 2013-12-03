__author__ = 'sulantha'

import networkx as nx
import numpy as np
from mayavi import mlab


def drawGraph(connectivityCSV, threshold):
    f = open(connectivityCSV)
    line = f.readline()
    numberOfNodes = len(str(line).split(','))
    f.close()

    G = nx.Graph()
    G.add_nodes_from(range(numberOfNodes))

    f = open(connectivityCSV)
    nodeSize = []
    for i in range(numberOfNodes):
        node_i_size = 0
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




def draw3dDPlot(p_x, p_y, p_z, graph, nodeSize):
    edge_size = 0.1
    node_scale = 0.01
    graph_colormap ='winter'
    pnts = mlab.points3d(np.array(p_x), np.array(p_y), np.array(p_z), nodeSize, scale_factor=node_scale, colormap=graph_colormap)
    pnts.mlab_source.dataset.lines = np.array(graph.edges())
    tube = mlab.pipeline.tube(pnts, tube_radius=edge_size)
    mlab.pipeline.surface(tube)
    #mlab.show()


def readPointsFromCSV(centroidsCSV):
    f = open(centroidsCSV)
    points_x = []
    points_y = []
    points_z = []
    for line in f.readlines():
        str_line = str(line).strip()
        points_x.append(float(str_line.split(',')[0]))
        points_y.append(float(str_line.split(',')[1]))
        points_z.append(float(str_line.split(',')[2]))
    return points_x, points_y, points_z

def addNetwork():
    p_x, p_y, p_z = readPointsFromCSV('Data/centroids_2000.csv')
    graph, nodeSize = drawGraph('Data/ad_connectivity.csv', 0.8)
    draw3dDPlot(p_x, p_y, p_z, graph, nodeSize)