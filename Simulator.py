#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May 03 20:55:07 2021
@author: krzysztof_skos
"""

import time
import matplotlib.pyplot as plt
from NanoNode import NanoNode
import Drawing
import numpy as np

veinDiameter = 4 # mm, max 10
nodeCount = 10
nodeList = []
# Generowanie nano urządzeń
for i in range(nodeCount):
    node = NanoNode(veinDiameter, [25, 0, veinDiameter / 2], 10)
    nodeList.append(node)
    #node.printData()

# Rysowanie wykresu
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#Drawing.drawPlot(veinDiameter/2, ax, nodeList)


# Logika programu
for x in np.arange(0, 50, 0.1):
    print("=================================")
    print("Printing nodes in step: " + str(x))
    for node in nodeList:
        node.flowStep(x)
        node.printData()
        print("***************")

    # Rysowanie wykresu
    #plt.close('all')
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    Drawing.drawPlot(veinDiameter / 2, ax, nodeList)
    time.sleep(1)