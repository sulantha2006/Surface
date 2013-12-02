__author__ = 'sulantha'

from numpy import array, random
from tvtk.api import tvtk
from mayavi import mlab
from mayavi.mlab import *


def polydata(pointsList, triangleList):
    # The numpy array data.
    points = array(pointsList, 'f')
    triangles = array(triangleList)
    scalars = random.random(points.shape)

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
    surf = mlab.pipeline.surface(dataset, opacity=0.1)
    mlab.pipeline.surface(mlab.pipeline.extract_edges(surf), color=(0, 0, 0), )

def readFile(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    pointsList = [map(float, x.split(' ')) for x in lines[1:int(lines[0])+1]]
    #triangleList = [map(int, y.split(' ')) for y in lines[int(lines[0])+2:len(lines)] if (max(map(int, y.split(' '))) - min(map(int, y.split(' '))) < 3)]
    triangleList = [map(int, y.split(' ')) for y in lines[int(lines[0])+2:len(lines)]]
    print len(triangleList)
    return pointsList, triangleList

pointsList, triangleList = readFile('SurfaceTemplates/BrainMesh_ICBM152_smoothed_tal.nv')
view(polydata(pointsList, triangleList))
mlab.show()