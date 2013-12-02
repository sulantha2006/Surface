__author__ = 'sulantha'

import numpy as np
from mayavi import mlab
from mayavi.mlab import *

#x, y, z = np.ogrid[-10:10:20j, -10:10:20j, -10:10:20j]
#s = np.sin(x*y*z)/(x*y*z)
#
#src = mlab.pipeline.scalar_field(s)
#mlab.pipeline.iso_surface(src, contours=[s.min()+0.1*s.ptp(), ], opacity=0.3)
#mlab.pipeline.iso_surface(src, contours=[s.max()-0.1*s.ptp(), ],)


def minc_reader(fname):
    #Reader for .mnc files.
    #Parameters:
    #fname -- Filename to be read.

    from tvtk.api import tvtk
    from mayavi.sources.vtk_data_source import VTKDataSource
    r = tvtk.MINCImageReader(file_name=fname)
    r.update()

    src = VTKDataSource(data=r.output)
    print src.data
    return src
from mayavi.api import Engine
e = Engine()
e.start()
s = e.new_scene()
source = minc_reader('/home/sulantha/Downloads/new_temp.mnc')
e.add_source(source)
from mayavi.modules.api import Surface
surf = Surface()
e.add_module(surf, obj=source)
mlab.show()

