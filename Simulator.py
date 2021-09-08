#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May 03 20:55:07 2021
@author: krzysztof_skos
"""
import math
import time
from datetime import datetime
import matplotlib.pyplot as plt
from NanoNode import NanoNode
import Drawing
import numpy as np
import csv
from random import randrange


transmissionTime = 64
drawPlot = False
simulationQuantity = 100
veinDiameter = 4  # mm, max 10
veinLength = 6  # mm
nodeTotal = 500000  # total number of nodes
latencyVariation = 0  # us, 0 for synchronous network

# Event counters and setting variables
maxOffset = 0  # max latency generated for simulation in us
brokenFrames = 0  # counter for frames broken due to collision
completedTransmissionCount = 0  # counter for completed transmissions
nodeCount = math.floor(
    math.pi * veinDiameter ** 2 * veinLength * nodeTotal / (22.4 * 10 ** 6))  # Simulated nodes

f = open('nodeCountTT64_simp1_gauss1000_2.csv', 'w')
writer = csv.writer(f)
writer.writerow(["Nodes total", "Nodes during each observation", "Broken frames due to collision", "Completed "
                                                                                                   "transmissions"])

t = time.time()
print(datetime.now().time())

for nt in range(100000, 2000000, 100):
    rowCounter += 1
    nodeTotal = nt
    tmp = randrange(0, 4, 1)
    #if tmp == 1:
    #    nodeCount = math.ceil(
    #        math.pi * veinDiameter ** 2 * veinLength * nodeTotal / (22.4 * 10 ** 6))  # Simulated nodes
    #else:
    #    nodeCount = math.floor(
    #        math.pi * veinDiameter ** 2 * veinLength * nodeTotal / (22.4 * 10 ** 6))
    nodeCount = math.floor(
                math.pi * veinDiameter ** 2 * veinLength * nodeTotal / (22.4 * 10 ** 6))
    if tmp == 0:
        nodeCount += 1
    elif tmp == 1:
        nodeCount -= 1
    brokenFrames = 0
    completedTransmissionCount = 0

    for z in range(simulationQuantity):
        maxOffset = 0
        nodeList = []
        sendingNodeList = []
        collision = False

        # Generating nano nodes and maxOffset
        for i in range(nodeCount):
            node = NanoNode(veinDiameter, veinLength, [0, veinDiameter / 2, veinLength - 2], latencyVariation + 1, i,
                            transmissionTime)
            nodeList.append(node)
            if node.offset > maxOffset:
                maxOffset = node.offset
            if node.inRouterRange and node.isSendingMessage:
                sendingNodeList.append(node)

        # Checking for collisions
        if len(sendingNodeList) > 1:
            for node in sendingNodeList:
                nodeList[node.id].setCollision(True)

        # Drawing start plot
        if drawPlot:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            Drawing.drawPlot(veinDiameter / 2 + 1, ax, nodeList, veinLength)  # Dlaczego promień+1?

        # Simulation - 1 us step
        for x in np.arange(0, transmissionTime + maxOffset, 1):
            sendingNodeList = []
            for node in nodeList:
                if node.inRouterRange and node.isSendingMessage:
                    sendingNodeList.append(node)
                node.flowStep()
            # Checking for collision each step
            if len(sendingNodeList) > 1:
                for nd in sendingNodeList:
                    nodeList[nd.id].setCollision(True)

        # Counting broken frames
        for node in nodeList:
            if node.collision:
                brokenFrames += 1

        # Counting completed transmissions
        if not collision:
            for node in nodeList:
                if node.commSuccess:
                    completedTransmissionCount += 1

        # Drawing end plot
        if drawPlot:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            Drawing.drawPlot(veinDiameter / 2 + 1, ax, nodeList, veinLength)

    writer.writerow([nt, nodeCount, brokenFrames, completedTransmissionCount])
print(time.time() - t)
