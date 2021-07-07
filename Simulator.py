#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May 03 20:55:07 2021
@author: krzysztof_skos
"""
import math
import time
import matplotlib.pyplot as plt
from NanoNode import NanoNode
import Drawing
import numpy as np

collisionCount = 0
veinDiameter = 4  # mm, max 10
veinLength = 6  # mm
nodeTotal = 100  # total number of nodes
nodeCount = math.floor(
    math.pi * veinDiameter * veinDiameter * veinLength * nodeTotal / (22.4 * 10 ** 2))  # Simulated nodes

for i in range(1000):
    nodeList = []
    sendingNodeListBeginning = []
    sendingNodeListEnd = []

    # Generowanie nano urządzeń
    for i in range(nodeCount):
        node = NanoNode(veinDiameter, veinLength, [0, veinDiameter / 2, veinLength - 2], 10)
        nodeList.append(node)
        if node.inRouterRange:
            sendingNodeListBeginning.append(node)
        # node.printData()

    # Sekcja sprawdzania kolizji
    if len(sendingNodeListBeginning) > 1:
        collisionCount += 1
        # break
    """
    # Rysowanie wykresu
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    Drawing.drawPlot(veinDiameter / 2, ax, nodeList, veinLength)
    """
    # Logika programu
    for x in np.arange(0, 64, 1):  # Symulacja - krok 1 us
        for node in nodeList:
            node.flowStep()
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    Drawing.drawPlot(veinDiameter / 2, ax, nodeList, veinLength)
    """
    for node in nodeList:
        if node.inRouterRange:
            sendingNodeListEnd.append(node)

    if len(sendingNodeListBeginning) != len(sendingNodeListEnd):
        collisionCount += 1
        # break
    else:
        for node in sendingNodeListBeginning:
            if node not in sendingNodeListEnd:
                collisionCount += 1
                break
print(collisionCount)