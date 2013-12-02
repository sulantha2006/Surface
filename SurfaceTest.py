__author__ = 'sulantha'

import numpy
from mayavi.mlab import *
from mayavi import mlab


def test_contour3d():
    x, y, z = numpy.ogrid[-100:100:1, -100:100:1, -100:100:1]
    scalars = (x*2*y*z*z)+(x*y*z)
    obj = contour3d(scalars, contours=4, transparent=True)
    return obj

test_contour3d()
mlab.show()



