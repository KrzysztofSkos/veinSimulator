#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May 03 20:55:07 2021
@author: krzysztof_skos
"""
import math
from random import uniform, randrange
from math import dist, cos, sin, pi

import numpy


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
    velocity = 1
    routerCoordinates = []
    collision = False
    id = 0

    def __init__(self, d, veinLength, routerCoordinates, offsetRange, iD, transmissionTime=64, v_sr=240):
        """
        Class constructor
        :param d: simulated vein diameter
        :param veinLength: simulated vein length
        :param routerCoordinates: list with 3 dimensional Euclidean coordinates
        :param offsetRange: max latency variation in us
        :param iD: node id
        :param transmissionTime: frame length
        :param v_sr: mean velocity of node in vein in mm/s
        """
        self.transmissionTime = transmissionTime
        self.id = iD
        self.drawCoordinates(d, veinLength)
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

    def drawCoordinates(self, d, veinLength):
        """

        :return:
        """
        self.R = d
        while self.R > d/2:
            self.coordinateY = uniform(-d/2, d/2)
            self.coordinateZ = uniform(-d/2, d/2)
            self.R = math.sqrt(self.coordinateY ** 2 + self.coordinateZ ** 2)
        self.x = uniform(0, veinLength)
        self.calculatePhi(self.coordinateY, self.coordinateZ)

    def calculatePhi(self, y, z):
        if y > 0 and z >= 0:
            self.phi = numpy.arctan(z / y)
        if y > 0 and z < 0:
            self.phi = numpy.arctan(z / y) + 2 * math.pi
        if y < 0:
            self.phi = numpy.arctan(z / y) + math.pi
        if y == 0 and z > 0:
            self.phi = math.pi / 2
        if y == 0 and z < 0:
            self.phi = 3 * math.pi / 2

    def checkRouterRange(self, routerCoordinates):
        """
        Method for checking if node is in router range
        :param routerCoordinates: list with 3 dimensional Euclidean coordinates
        :return: True if node is in router range, False otherwise
        """
        if dist(routerCoordinates, [self.coordinateY, self.coordinateZ, self.x]) < 2:
            return True
        else:
            return False

    def flowStep(self):
        """
        Method that defines node behavior during blood flow in 1us
        :return: -
        """
        self.x += self.velocity
        if self.transmissionTime >= 0:
            if self.offset > 0:
                self.offset -= 1
            if self.offset <= 0:
                self.isSendingMessage = True
                self.transmissionTime -= 1
            self.inRouterRange = self.checkRouterRange(self.routerCoordinates)
            if self.transmissionTime == 0 and self.inRouterRange and not self.collision:
                self.commSuccess = True
        else:
            self.isSendingMessage = False

    def setCollision(self, collision):
        """
        Collision setter
        :param collision: True/False
        :return: -
        """
        self.collision = collision

    def printData(self):
        """
        Method for printing node data in console
        :return:
        """
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
