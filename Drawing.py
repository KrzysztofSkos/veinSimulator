#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on May 11 22:42:06 2021
@author: krzysztof_skos
"""

import matplotlib.pyplot as plt
import numpy as np


def data_for_cylinder_along_z(center_x, center_y, radius, height_z):
    """
    Method for creating grid for cylinder drawing. Cylinder will be created along Z axis
    :param center_x: Euclidean 3 dimensional center of drawing on X axis
    :param center_y: Euclidean 3 dimensional center of drawing on Y axis
    :param radius: cylinder radius
    :param height_z: cylinder height
    :return: Three lists with grid coordinates for z, y, x sequentially
    """
    z = np.linspace(0, height_z, 50)
    theta = np.linspace(0, 2 * np.pi, 50)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = radius * np.cos(theta_grid) + center_x
    y_grid = radius * np.sin(theta_grid) + center_y
    return z_grid, y_grid, x_grid


def drawPlot(rad, ax, nodeList, length):
    """
    Method for drawing plot during simulation
    :param rad: vein radius
    :param ax: instance of figure() with subplot
    :param nodeList: list of nodes to draw
    :param length: cylinder length
    :return:
    """
    ax.clear()
    ax.scatter(length-2, 0, rad, marker="o")  # router
    ax.text(length - 1.9, 0, rad, "router")
    for node in nodeList:
        if node.x <= length:
            if node.inRouterRange:
                if node.isSendingMessage:
                    ax.scatter(node.x, node.coordinateY, node.coordinateZ, marker="d", c="#00ff02")
                else:
                    ax.scatter(node.x, node.coordinateY, node.coordinateZ, marker="x", c="#00ff02")
            else:
                if node.isSendingMessage:
                    ax.scatter(node.x, node.coordinateY, node.coordinateZ, marker="d", c="Red")
                else:
                    ax.scatter(node.x, node.coordinateY, node.coordinateZ, marker="x", c="Red")

    xc, yc, zc = data_for_cylinder_along_z(0, 0, rad, length)
    ax.plot_surface(xc, yc, zc, alpha=0.5)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()
