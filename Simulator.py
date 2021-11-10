#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May 03 20:55:07 2021
@author: krzysztof_skos
"""
import math
from datetime import datetime
from NanoNode import NanoNode
import matplotlib.pyplot as plt
import Drawing
import numpy as np
import csv

drawPlot = False
transmissionTime = 64
simulationQuantity = 1000
veinLength = 6  # mm
bloodVolume = 5*10**6
veinDiameter = 4
nodeTotal = 500000  # total number of nodes
latencyVariation = 0  # ms * 10 # us, 0 for synchronous network
prob = 1 / (240 * 60)
prob_a = math.pi * veinDiameter ** 2 * veinLength / (4 * bloodVolume)

# Event counters and setting variables
maxOffset = 0  # max latency generated for simulation in us
brokenFrames = 0  # counter for frames broken due to collision
completedTransmissionCount = 0  # counter for completed transmissions
nodeCount = math.floor(
    math.pi * veinDiameter ** 2 * veinLength * nodeTotal / (4 * bloodVolume))  # Simulated nodes

f = open('../Results/pierwsze_wyniki/scenariusz2/nodeCount_sync_vein15.csv', 'w')
writer = csv.writer(f)
writer.writerow(["Nodes total", "Nodes during each observation", "Broken frames due to collision", "Completed "
                                                                                                   "transmissions"])

print(datetime.now().time())
data = []

for nt in range(1000, 4000000, 1000):
    nodeTotal = nt
    nodeCountBase = math.pi * veinDiameter ** 2 * veinLength * nodeTotal / (4 * bloodVolume)
    nodeCountList = []
    brokenFrames = 0
    completedTransmissionCount = 0

    for z in range(simulationQuantity):
        nodeCount = np.random.binomial(nt, prob_a, 1)[0]
        nodeCountList.append(nodeCount)
        maxOffset = 0
        nodeList = []
        sendingNodeList = []
        collision = False

        # Generating nano nodes and maxOffset
        for i in range(nodeCount):
            node = NanoNode(veinDiameter, veinLength, [0, veinDiameter / 2, veinLength - 1.5], latencyVariation + 1, i,
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
            Drawing.drawPlot(veinDiameter / 2 + 1, ax, nodeList, veinLength)

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

        # Drawing end plot
        if drawPlot:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            Drawing.drawPlot(veinDiameter / 2 + 1, ax, nodeList, veinLength)

        # Counting broken frames
        for node in nodeList:
            if node.collision:
                brokenFrames += 1
#                collision = True

        # Counting completed transmissions
        if not collision:
            for node in nodeList:
                if node.commSuccess:
                    completedTransmissionCount += 1

    # data.append([nt, nodeCount, brokenFrames, completedTransmissionCount])
    writer.writerow([nt, np.mean(nodeCountList), brokenFrames, completedTransmissionCount])

# writer.writerows(data)
print(datetime.now().time())
