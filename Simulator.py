#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May 03 20:55:07 2021
@author: krzysztof_skos
"""
import math
import time
from datetime import datetime
from NanoNode import NanoNode
import numpy as np
import csv

transmissionTime = 64
simulationQuantity = 60
veinLength = 6  # mm
#veinDiameter = math.sqrt(2.8 * 10**5 / (3 * math.pi * veinLength))  # mm, max 10
veinDiameter = math.sqrt(1.4 * 10**4 / (9 * math.pi * veinLength))
print("Diameter: ", veinDiameter)
nodeTotal = 500000  # total number of nodes
latencyVariation = 0  # us, 0 for synchronous network

# Event counters and setting variables
maxOffset = 0  # max latency generated for simulation in us
brokenFrames = 0  # counter for frames broken due to collision
completedTransmissionCount = 0  # counter for completed transmissions
nodeCount = math.floor(
    math.pi * veinDiameter ** 2 * veinLength * nodeTotal / (22.4 * 10 ** 6))  # Simulated nodes

f = open('nodeCountTT64_simp05_off0_1.csv', 'w')
writer = csv.writer(f)
writer.writerow(["Nodes total", "Nodes during each observation", "Broken frames due to collision", "Completed "
                                                                                                   "transmissions"])

t = time.time()
print(datetime.now().time())
data = []

for nt in range(1000, 2000000, 1000):
    nodeTotal = nt
    nodeCount = round(math.pi * veinDiameter ** 2 * veinLength * nodeTotal / (22.4 * 10 ** 6))
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
                collision = True

        # Counting completed transmissions
        if not collision:
            for node in nodeList:
                if node.commSuccess:
                    completedTransmissionCount += 1

    #data.append([nt, nodeCount, brokenFrames, completedTransmissionCount])
    writer.writerow([nt, nodeCount, brokenFrames, completedTransmissionCount])
#writer.writerows(data)
print(time.time() - t)
