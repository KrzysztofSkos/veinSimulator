#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May 03 20:55:07 2021
@author: krzysztof_skos
"""

import random
import math
from random import uniform, randrange
from math import dist


class NanoNode:
    coordinates = [0, 0]  # x and y
    z = 0.0
    R = 0.0  # distance from vein center
    inRouterRange = False
    isSendingMessage = True
    offset = 0
    commSuccess = False

    def __init__(self, d, routerCoordinates, offsetRange, routerRange):
        # d - vein diameter
        self.coordinates[0] = uniform(-d / 2, d / 2)
        self.coordinates[1] = uniform(-d / 2, d / 2)
        self.R = dist(self.coordinates, [0, 0])
        self.offset = randrange(offsetRange)
        self.commSuccess = False
        if self.offset == 0:
            self.isSendingMessage = True
        else:
            self.isSendingMessage = False

        if dist(routerCoordinates, [self.coordinates[0], self.coordinates[1], self.z]) < routerRange:
            self.inRouterRange = True
        else:
            self.inRouterRange = False

    def printData(self):
        print("Printing info about node")
        print("x: " + str(self.coordinates[0]))
        print("y: " + str(self.coordinates[1]))
        print("z: " + str(self.z))
        print("Distance from vein center: " + str(self.R))
        print("Offset: " + str(self.offset))
        print("Is sending message? " + str(self.isSendingMessage))
        print("In router range? " + str(self.inRouterRange))


