__author__ = 'sulantha'

from scipy import cluster
import numpy as np
from mayavi import mlab
from mayavi.mlab import *


def readFile(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    pointsList = [map(float, x.split(' ')) for x in lines[1:int(lines[0])+1]]
    #triangleList = [map(int, y.split(' ')) for y in lines[int(lines[0])+2:len(lines)] if (max(map(int, y.split(' '))) - min(map(int, y.split(' '))) < 3)]
    triangleList = [[int(k)-1 for k in y.split(' ')] for y in lines[int(lines[0])+2:len(lines)]]
    return pointsList, triangleList

p, t = readFile('Templates/BrainMesh_ICBM152.nv')
c, l = cluster.vq.kmeans2(np.array(p), 2000, iter=5, minit='points')
p_x = zip(*c)[0]
p_y = zip(*c)[1]
p_z = zip(*c)[2]
pnts = mlab.points3d(np.array(p_x), np.array(p_y), np.array(p_z), np.ones(2000), scale_factor=1)


np.save('Data/centroids_new.npy', c)
np.save('Data/labels_new.npy', l)
mlab.show()



