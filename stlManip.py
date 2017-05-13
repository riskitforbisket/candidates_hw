'''
    Author: Daniel Irizarry

    CALIBRATION VARIABLES:
        -RANGE = distance in 1 direction from 0, RANGE = 3 would be (-3,3)
        -NPTS = number of points in the above RANGE
        -OUT_FILENAME = yup. (no extension necesary)
        -MATPLOTLIB_VIS = a debug flad to view the results of the triangulation
            in a mpl plot before pulling it into blender
        - DO_GAUSS = a flag used to quickly produce the gaussian curve, this
            was used for easy of testing the code without tedius commandline
            text. make 0 to enter function from CMDLINE or 1 for garbage CMD
            input.

    The Problem:
        Generate a STL file from any given multivariable expression.

    The Approach:
        This one took a bit of research to first learn what the STL file
        format was and also to find a tool to read and write them. After
        a decent amount of time fiddling with tools I quit them and just
        wrote my own very very simple STL writer.

        The write only creates an ASCII STL file so that I could visually
        inspect the file to ensure formating. The algorithm uses Python's
        native ecal() function which requires X/Y to be known. Those are
        passed to the Delaunay function to create triangles and then the
        mesh is created using the 3D coords and the triangle triplets.

'''

import numpy as np

#triangulation function and alias
from scipy.spatial import Delaunay as ssd

#for easy frame visualization
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#calibration variables
RANGE = 3
NPTS = 100
OUT_FILENAME = "Dirizary_STL_sample"
MATPLOTLIB_VIS = 1
DO_GAUSS = 0

#I realize that this function is not needed but it keeps the code
#cleaner and more organised as long as performance is not an issue
def writeSTLToFile(tri, points):
    fp = open(OUT_FILENAME+".stl", 'w')

    #write necesary ascii header line
    print>>fp, "solid surface"

    #write my triangles to a file
    #normal calculation could be done here but some visual software
    #will calculate them for you. (so says the internet)
    normal = "0.0 0.0 0.0\n"
    for i in range(0, len(tri.simplices)):
        print>>fp, "facet normal " + normal
        print>>fp, "   outer loop"
        print>>fp, "      vertex ", str(points[tri.simplices[i,0], 0]) + " " + str(points[tri.simplices[i,0], 1]) + " " + str(points[tri.simplices[i,0], 2])
        print>>fp, "      vertex ", str(points[tri.simplices[i,1], 0]) + " " + str(points[tri.simplices[i,1], 1]) + " " + str(points[tri.simplices[i,1], 2])
        print>>fp, "      vertex ", str(points[tri.simplices[i,2], 0]) + " " + str(points[tri.simplices[i,2], 1]) + " " + str(points[tri.simplices[i,2], 2])
        print>>fp, "   endloop"
        print>>fp, "endfacet"
    fp.close()
    return

def makeSTL(points, vis):

    #perform Delauney triangulation on the 3d points because it is
    #readily available through numpy
    tri = ssd(points[:,:2])

    writeSTLToFile(tri, points)

    #visualize the computed surface at a glance
    if vis:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_trisurf(points[:,0],points[:,1],points[:,2], triangles=tri.simplices)
        plt.show()
    return

if __name__ == "__main__":
    #Let them know the truth
    print "Daniel Irizarry - The Best!"

    #statically define the mesh NPTS since it was not specified
    #xax = np.arange(NPTS)
    #yax = np.arange(NPTS)
    xax = np.linspace(-RANGE,RANGE,NPTS)
    yax = np.linspace(-RANGE,RANGE,NPTS)
    x, y = np.meshgrid(xax,yax)

    #get commandline input, echo, eval
    #GAUSSIAN plot is there for testing the code
    fxn = raw_input("Enter your function: ")
    print fxn
    if not DO_GAUSS:
        surface = eval(fxn)
    else:
        surface = (1/np.sqrt(2*np.pi)**np.exp(-(x**2/2)-(y**2/2)))*25

    points = []
    for i in range(0,NPTS):
        for j in range(0,NPTS):
            #form vertex arrays and shift the mesh to center XY on 0,0
            points.append([xax[i],yax[j],surface[i,j]])

    #write out cvs of x,y,z points
    pointsArr = np.array(points)
    np.savetxt("surfacePoints.csv", pointsArr, delimiter=',')

    #convert data to STL formate
    myMesh = makeSTL(pointsArr, MATPLOTLIB_VIS)
