#!/usr/bin/python3
"""
Author:     Konstantinos Liosis
File:       calc_dist.py
Desc:       calculate the square area around a point on the map
"""

import math
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
DEG2DIST = int(config['CONST']['deg2dist'])


def dist(point: tuple, distance: float):
    """
    Calculates the borders of a square of size 2*distance and point as its centroid (in kilometers)
    :param point: The centroid point on the map. (lat, lon)
    :param distance: The distance of the furthest NSEW points
    :return: the borders of the square in lat, lon values
    """

    # https://gis.stackexchange.com/questions/142326/calculating-longitude-length-in-miles
    coef = DEG2DIST
    d_lat = abs(point[0] - distance / coef)
    coef = coef * math.cos(math.radians(point[0]))
    d_lon = abs(point[1] - distance / coef)
    latN = point[0] + (point[0] - d_lat)
    latS = d_lat
    lonE = point[1] + (point[1] - d_lon)
    lonW = d_lon

    # invoke map_img to create image. Greece is hardcoded because of the nature of our data
    # Future feature, module issues
    # map_img([latN, latN, latS, latS], [lonE, lonW, lonE, lonW], "Greece")

    return latN, latS, lonE, lonW
