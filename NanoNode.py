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
    coordinateY = 0
    coordinateZ = 0
    x = 0.0
    R = 0.0  # distance from vein center
    phi = 0.0  # angle
    inRouterRange = False
    isSendingMessage = True
    offset = 0  # us
    commSuccess = False
    transmissionTime = 64
    velocity = 1
    routerCoordinates = []
    collision = False
    id = 0

    def __init__(self, d, veinLength, routerCoordinates, offsetRange, id, v_sr=200):
        # d - vein diameter
        # l - simulated vein length
        self.id = id
        self.phi = uniform(0, 2 * pi)
        self.R = uniform(0, d / 2)
        self.x = uniform(0, veinLength)
        self.coordinateY = self.R * cos(self.phi)
        self.coordinateZ = self.R * sin(self.phi)
        self.velocity = v_sr * 2 * ((d / 2) ** 2 - self.R ** 2) / ((d / 2) ** 2)
        self.velocity = self.velocity / 10 ** 6  # Zmiana prędkości z mm/s na mm/us
        self.offset = randrange(offsetRange)
        self.commSuccess = False
        if self.offset == 0:
            self.isSendingMessage = True
        else:
            self.isSendingMessage = False
        self.routerCoordinates = routerCoordinates
        self.inRouterRange = self.checkRouterRange(routerCoordinates)

    def checkRouterRange(self, routerCoordinates):
        if dist(routerCoordinates, [self.coordinateY, self.coordinateZ, self.x]) < 2:
            return True
        else:
            return False

    def flowStep(self):
        self.x += self.velocity
        if self.transmissionTime >= 0 and not self.collision:
            if self.offset > 0:
                self.offset -= 1
            if self.offset <= 0:
                self.isSendingMessage = True
                self.transmissionTime -= 1
            self.inRouterRange = self.checkRouterRange(self.routerCoordinates)
            if self.transmissionTime == 0 and self.inRouterRange:
                self.commSuccess = True
        else:
            self.isSendingMessage = False

    def setCollision(self, collision):
        self.collision = collision

    def checkTransmission(self):
        if not self.commSuccess:
            if self.isSendingMessage:
                if dist([self.x, self.coordinateY, self.coordinateZ],
                        [26, 0, 2]) < 2:  # temp - router coordinates & range
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
        print("================================")
