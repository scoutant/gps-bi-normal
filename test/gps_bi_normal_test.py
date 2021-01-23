import unittest
from math import exp

from gps_bi_normal import Point, meters_per_degree
from gps_bi_normal import generate
import matplotlib.pyplot as plt
import numpy as np

Eyjafjallajökull = Point(63.629256, -19.607135) # Volcano in Iceland

class GenerateTest(unittest.TestCase):
    def test_generate_10_points(self):
        points = generate( Eyjafjallajökull, 1000, size=10) # 1000 m standard deviation
        self.assertTrue(len(points)==10)
        for p in points:
            print( p, p.distance_to(Eyjafjallajökull))
            self.assertTrue( p.distance_to(Eyjafjallajökull)<3000)

    def test_proportion_three_sigma(self):
        points = generate( Eyjafjallajökull, 1000, size=1000)
        self.assertTrue(len(points)==1000)
        counter=0
        for p in points:
            if p.distance_to(Eyjafjallajökull) > 3000:
                counter+=1
        print("counter", counter)
        self.assertTrue( 5 < counter <12) # proportion of points away from 3*sigma, usually within [0.5%,1%]...

    def test_write_csv(self):
        points = generate( Eyjafjallajökull, 1000, size=1000)
        with open('points.csv', 'w') as out:
            # out.write( "timestamp;type;latitude;longitude;accuracy;moving")
            out.write("latitude,longitude")
            for p in points:
                out.write( f"\n{p.csv}")

    def test_display_3d(self):
        sigma=1000 # in meters
        x = np.linspace(63.60, 63.66, 50)
        y = np.linspace(-19.66, -19.56, 50)
        X, Y = np.meshgrid(x, y)  # X and Y are 2 matrices, shape 50x50
        Z = np.zeros((50, 50))
        o = Eyjafjallajökull
        sa = sigma/meters_per_degree
        latitude_radian = np.radians(o.latitude)
        so = sa / np.cos(latitude_radian)  # np.cos() operates in radians

        for i in range(50):
            for j in range(50):
                momentum = ((x[i]-o.latitude)/sa)**2 + ((y[j]-o.longitude)/so)**2
                Z[j][i] = exp( -momentum  )

        ax = plt.axes(projection='3d')
        ax.contour3D(X, Y, Z, 50, cmap='binary')
        ax.view_init(20, -85)  # initialize point of view
        plt.show()

    def test_display_mayavi(self):
        sigma=1000 # in meters
        steps=50
        X, Y = np.meshgrid( np.linspace(63.60, 63.66, steps), np.linspace(-19.66, -19.56, steps))
        Z = np.zeros((steps, steps))
        o = Eyjafjallajökull
        sa = sigma/meters_per_degree
        latitude_radian = np.radians(o.latitude)
        so = sa / np.cos(latitude_radian)  # np.cos() operates in radians
        for i in range(steps):
            for j in range(steps):
                momentum = ((X[j][i]-o.latitude)/sa)**2 + ((Y[j][i]-o.longitude)/so)**2
                Z[j][i] = exp( -momentum )/20 # scaling for nicer display
        from mayavi import mlab
        s = mlab.mesh(X, Y, Z)
        mlab.show()