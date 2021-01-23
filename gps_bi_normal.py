from __future__ import annotations # so as to enable to reference enclosed type, no more necessary with python 3.10+
import numpy as np
from typing import List # no more necessary with python 3.9+
import geopy.distance

meters_per_degree = 40007000 / 360

class Point:
    """ Like Google LatLng. Caution do not mix with geopy.Point """
    def __init__(self, latitude:float, longitude:float):
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self): # overloading to string method
        return f"{self.latitude:.5f};{self.longitude:.5f}"

    def sum(self, other:Point):
        self.latitude += other.latitude
        self.longitude += other.longitude

    def __add__(self, b:Point):
        """ overriding operator, use like so : z = a + b """
        return Point( self.latitude + b.latitude, self.longitude + b.longitude)

    def __iadd__(self, b:Point):
        """ in place operator, https://docs.python.org/fr/3.9/library/operator.html. Enabling : p+=q """
        self.latitude += b.latitude
        self.longitude += b.longitude
        return self

    def distance_to(self,other:Point)->float:
        """ :returns geodesic distance in meters """
        return geopy.distance.geodesic(self.tuple, other.tuple).meters

    @property
    def tuple(self):
        """ :returns itself as a tuple, latitude first """
        return self.latitude, self.longitude

    @property
    def csv(self)->str:
        """ :returns itself as a string for csv file """
        return f"{self.latitude:.5f},{self.longitude:.5f}"

def generate(center:Point, sigma:float, size:int=100) -> List[Point]:
    """ generate a list of Points with given standard deviation in meters """
    print(f"generating {size} points around {center} with standard deviation {sigma} m")
    sa = sigma/meters_per_degree
    latitude_radian = np.radians( center.latitude)
    so = sa / np.cos(latitude_radian) # np.cos() operates in radians
    cov = [[sa*sa, 0],
           [0, so*so ]]
    array = np.random.multivariate_normal([center.latitude,center.longitude], cov, size=size)
    points : List[Point] = []
    for p in array:
        points.append( Point(p[0],p[1]))
    return points
