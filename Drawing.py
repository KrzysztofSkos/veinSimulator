#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May 11 22:42:06 2021
@author: krzysztof_skos
"""

import matplotlib.pyplot as plt
import numpy as np
import NanoNode
from mpl_toolkits.mplot3d import Axes3D


def __init__():
    fig = plt.figure()


def data_for_cylinder_along_z(center_x, center_y, radius, height_z):
    z = np.linspace(0, height_z, 50)
    theta = np.linspace(0, 2 * np.pi, 50)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = radius * np.cos(theta_grid) + center_x
    y_grid = radius * np.sin(theta_grid) + center_y
    return z_grid, y_grid, x_grid


def drawPlot(rad, ax, nodeList, length):
    """

    :param rad: vein radius
    :param ax:
    :param nodeList:
    :return:
    """
    ax.clear()
    ax.scatter(length-2, 0, rad, marker="o")  # router
    ax.text(length - 1.9, 0, rad, "router")
    for node in nodeList:
        if node.x <= length:
            if node.inRouterRange:
                ax.scatter(node.x, node.coordinateY, node.coordinateZ, marker="d", c="#00ff02")
            else:
                ax.scatter(node.x, node.coordinateY, node.coordinateZ, marker="d", c="Red")
    #plt.legend(loc='upper left')

    Xc, Yc, Zc = data_for_cylinder_along_z(0, 0, rad, length)
    ax.plot_surface(Xc, Yc, Zc, alpha=0.5)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()
