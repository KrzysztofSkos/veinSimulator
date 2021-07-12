#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May 03 20:55:07 2021
@author: krzysztof_skos
"""
import math
import matplotlib.pyplot as plt
from NanoNode import NanoNode
import Drawing
import numpy as np

drawPlot = True
maxOffset = 0
collisionCount = 0
brokenFrames = 0
completedTransmissionCount = 0
veinDiameter = 4  # mm, max 10
veinLength = 6  # mm
nodeTotal = 500000  # total number of nodes
nodeCount = math.floor(
    math.pi * veinDiameter**2 * veinLength * nodeTotal / (22.4 * 10**6))  # Simulated nodes

print("Nodes during observation: ", nodeCount)

for z in range(1):
    nodeList = []
    sendingNodeList = []
    collision = False

    # Generowanie nano urządzeń
    for i in range(nodeCount):
        node = NanoNode(veinDiameter, veinLength, [0, veinDiameter / 2, veinLength - 2], 10, i)
        nodeList.append(node)
        if node.offset > maxOffset:
            maxOffset = node.offset
        if node.inRouterRange and node.isSendingMessage:
            sendingNodeList.append(node)

    # Sekcja sprawdzania kolizji
    if len(sendingNodeList) > 1:
        for node in sendingNodeList:
            nodeList[node.id].setCollision(True)
        # collisionCount += 1
        # collision = True
        # continue

    if drawPlot:
        # Rysowanie wykresu
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        Drawing.drawPlot(veinDiameter / 2 + 1, ax, nodeList, veinLength)  # Dlaczego promień+1?

    # Logika programu
    for x in np.arange(0, 64+maxOffset, 1):  # Symulacja - krok 1 us
        sendingNodeList = []
        for node in nodeList:
            if node.inRouterRange and node.isSendingMessage:
                sendingNodeList.append(node)

            node.flowStep()
        if len(sendingNodeList) > 1:
            for nd in nodeList:
                nodeList[nd.id].setCollision(True)
        #    collisionCount += 1
        #    collision = True
        #    break

    for node in nodeList:
        if node.collision:
            brokenFrames += 1

    if not collision:
        for node in nodeList:
            if node.commSuccess:
                completedTransmissionCount += 1

    if drawPlot:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        Drawing.drawPlot(veinDiameter / 2 + 1, ax, nodeList, veinLength)

print("Broken frames due to collision: ", brokenFrames)
print("Completed transmissions: ", completedTransmissionCount)
