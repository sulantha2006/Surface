__author__ = 'sulantha'

from scipy import cluster
import numpy as np
import networkx as nx
from tvtk.api import tvtk
from mayavi import mlab
from mayavi.mlab import *


def readTemplateFile(templateFile):
    with open(templateFile) as f:
        lines = f.read().splitlines()
    pointsList = [map(float, x.split(' ')) for x in lines[1:int(lines[0])+1]]
    triangleList = [[int(k)-1 for k in y.split(' ')] for y in lines[int(lines[0])+2:len(lines)]]
    return pointsList, triangleList


def performClustering(pointsList, numberOfClusters):
    centroids, labels = cluster.vq.kmeans2(np.array(pointsList), numberOfClusters, iter=5, minit='random')
    return centroids, labels

def viewPoints(pointsOnGraph):
    p_x = zip(*pointsOnGraph)[0]
    p_y = zip(*pointsOnGraph)[1]
    p_z = zip(*pointsOnGraph)[2]
    nodeSize = np.random.random(2000)
    edge_size = 0.1
    node_scale = 0.1
    graph_colormap ='winter'
    pnts = mlab.points3d(np.array(p_x), np.array(p_y), np.array(p_z), nodeSize, scale_factor=node_scale, colormap=graph_colormap)
    mlab.pipeline.surface(pnts)


pointsList, triangleList = readTemplateFile('Templates/BrainMesh_ICBM152_smoothed.nv')
centroids, labels = performClustering(pointsList, 2000)
viewPoints(centroids)
mlab.show()