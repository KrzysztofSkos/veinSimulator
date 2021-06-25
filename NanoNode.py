#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May 03 20:55:07 2021
@author: krzysztof_skos
"""

import random
import math
from random import uniform, randrange
from math import dist, cos, sin, pi


class NanoNode:
    coordinates = [0, 0]  # y and z
    coordinateY = 0
    coordinateZ = 0
    x = 0.0
    R = 0.0  # distance from vein center
    phi = 0.0 # angle
    inRouterRange = False
    isSendingMessage = True
    offset = 0
    commSuccess = False
    transmissionTime = 10
    velocity = 1

    def __init__(self, d, routerCoordinates, offsetRange):
        # d - vein diameter
        self.phi = uniform(0, 2*pi)
        self.R = uniform(0, d/2)
        self.coordinateY = self.R * cos(self.phi)
        self.coordinateZ = self.R * sin(self.phi)
        self.velocity = -self.R*self.R + d*d/4 + 1 # 1 - bazowa prędkość przy ścianie żyły
        self.offset = randrange(offsetRange)
        self.commSuccess = False
        if self.offset == 0:
            self.isSendingMessage = True
        else:
            self.isSendingMessage = False

        if dist(routerCoordinates, [self.coordinateY, self.coordinateZ, self.x]) < 2: #2 = zasięg rutera - stała
            self.inRouterRange = True
        else:
            self.inRouterRange = False

    def flowStep(self, x):
        self.x += self.velocity * x
        if self.offset > 0:
            self.offset -= 1
        if self.offset <= 0:
            self.isSendingMessage = True
        self.checkTransmission()

    def checkTransmission(self):
        if not self.commSuccess:
            if self.isSendingMessage:
                if dist([self.x, self.coordinateY, self.coordinateZ], [26, 0, 2]) < 2: #temp - router coordinates & range
                    self.transmissionTime -= 1
            if self.transmissionTime == 0:
                self.commSuccess = True
                self.isSendingMessage = False

    def printData(self):
        print("Printing info about node")
        print("y: " + str(self.coordinateY))
        print("z: " + str(self.coordinateZ))
        print("x: " + str(self.x))
        print("Distance from vein center: " + str(self.R))
        print("Offset: " + str(self.offset))
        print("Is sending message? " + str(self.isSendingMessage))
        print("In router range? " + str(self.inRouterRange))
        print("Transmission time: " + str(self.transmissionTime))
        print("Communication succeded? " + str(self.commSuccess))


