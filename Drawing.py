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


def drawPlot(rad, ax, nodeList):
    """

    :param rad: vein radius
    :param ax:
    :param nodeList:
    :return:
    """
    ax.clear()
    ax.scatter(25, 0, rad)
    for node in nodeList:
        ax.scatter(node.x, node.coordinateY, node.coordinateZ)
    #plt.legend(loc='upper left')

    ax.text(26, 0, rad, "router")

    Xc, Yc, Zc = data_for_cylinder_along_z(0, 0, rad, 50)
    ax.plot_surface(Xc, Yc, Zc, alpha=0.5)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()
