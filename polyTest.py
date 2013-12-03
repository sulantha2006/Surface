__author__ = 'sulantha'

from numpy import array, random
from tvtk.api import tvtk
from mayavi import mlab
from mayavi.mlab import *
import itertools
import DrawGraph


def polydata(pointsList, triangleList):
    # The numpy array data.
    points = array(pointsList, 'f')
    triangles = array(triangleList)
    #scalars = random.random(points.shape)
    #scalars_t = [list(itertools.repeat(i+1, 40)) for i in range(2001)]
    scalars_t = [list(itertools.repeat(int(value)+1, 40)) for value in open('Data/ad_full_sum.csv').read().split(',')]
    scalars_t2 = [item for sublist in scalars_t for item in sublist]
    scalars = scalars_t2[0:81923]


    # The TVTK dataset.
    mesh = tvtk.PolyData(points=points, polys=triangles)
    mesh.point_data.scalars = scalars
    mesh.point_data.scalars.name = 'scalars'
    return mesh


def view(dataset):
    """ Open up a mayavi scene and display the dataset in it.
    """
    fig = mlab.figure(bgcolor=(1, 1, 1), fgcolor=(0, 0, 0),
                      figure=dataset.class_name[3:])
    surf = mlab.pipeline.surface(dataset, opacity=0.3)
    #mlab.pipeline.surface(mlab.pipeline.extract_edges(surf), color=(0, 0, 0), )

def readFile(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    pointsList = [map(float, x.split(' ')) for x in lines[1:int(lines[0])+1]]
    #triangleList = [map(int, y.split(' ')) for y in lines[int(lines[0])+2:len(lines)] if (max(map(int, y.split(' '))) - min(map(int, y.split(' '))) < 3)]
    triangleList = [[int(k)-1 for k in y.split(' ')] for y in lines[int(lines[0])+2:len(lines)]]
    return pointsList, triangleList

pointsList, triangleList = readFile('Templates/BrainMesh_ICBM152.nv')
view(polydata(pointsList, triangleList))
DrawGraph.addNetwork()
mlab.show()
