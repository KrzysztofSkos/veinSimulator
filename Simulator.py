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

# node = NanoNode(10, [10, 10, 10], 10, 1)
# node.printData()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for i in range(3, 10):
    print(i)
    Drawing.drawPlot(i, ax)
    time.sleep(1)
