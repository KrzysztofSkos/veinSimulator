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
simulationQuantity = 1000
veinLength = 6  # mm
bloodVolume = 4.8*10**6
veinDiameter = 2 * math.sqrt(bloodVolume / (240 * 60 * math.pi * 1))
print("Diameter: ", veinDiameter)
nodeTotal = 500000  # total number of nodes
latencyVariation = 0  # us, 0 for synchronous network
prob = 1 / (240 * 60)
prob_a = math.pi * veinDiameter ** 2 * veinLength / (4 * bloodVolume)

# Event counters and setting variables
maxOffset = 0  # max latency generated for simulation in us
brokenFrames = 0  # counter for frames broken due to collision
completedTransmissionCount = 0  # counter for completed transmissions
nodeCount = math.floor(
    math.pi * veinDiameter ** 2 * veinLength * nodeTotal / (4 * bloodVolume))  # Simulated nodes

f = open('../Results/distribution/nodeCount_bernoulli_wrong.csv', 'w')
writer = csv.writer(f)
writer.writerow(["Nodes total", "Nodes during each observation", "Broken frames due to collision", "Completed "
                                                                                                   "transmissions"])

t = time.time()
print(datetime.now().time())
data = []

for nt in range(1000, 100000, 100):
    nodeTotal = nt
    nodeCountBase = math.pi * veinDiameter ** 2 * veinLength * nodeTotal / (4 * bloodVolume)
    nodeCountList = []
    brokenFrames = 0
    completedTransmissionCount = 0

    for z in range(simulationQuantity):
        # nodeCount = round(nodeCountBase + np.random.normal(0, 0.3, 1)[0])
        # nodeCount = round(np.random.normal(nt, 0.001*nt, 1)[0])
        # nodeCount = np.random.binomial(nt, prob_a, 1)[0]
        nodeCount = round(nodeCountBase + np.random.binomial(10, 0.33, 1)[0]/10)
        nodeCountList.append(nodeCount)
        maxOffset = 0
        nodeList = []
        sendingNodeList = []
        collision = False

        # Generating nano nodes and maxOffset
        for i in range(nodeCount):
            node = NanoNode(veinDiameter, veinLength, [0, veinDiameter / 2, veinLength - 0.5], latencyVariation + 1, i,
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
    writer.writerow([nt, np.mean(nodeCountList), brokenFrames, completedTransmissionCount])
#writer.writerows(data)
print(time.time() - t)
