# veinSimulator

The veinSimulator is a simulation tool created for the engeneering authors thesis, where the detailed descriptiom is provided.

The simulator is composed of 3 main components:

- the Vein fragment – a cylinder of a given diameter and length
- the Nano router (that covers a sphere with given radius)
- the Nano nodes flowing in direction of X axis

veinSimulator simulates a vein ragment with one nano router pleced in the vein area. The nano nodes are generated in the vein and their flow and transmission are observed.

The tool is composed of three classes/files. Simulator, NanoNode and Drawing.

The Simulator.py is a core of the simulation that processes all of the parameters.

The NanoNode.py is a class that processes and controls the transmission time and position change for each node.

The Drawing.py is responsible for drawing plot of thee vein with the nodes and the router.

The simulator generates a csv file with four columns with data. Starting from first:

- Nodes total
- Nodes during each observation
- Broken frames due to collision
- Completed transmissions

## Requirements

veinSimulator requires Python 3.0 and folowing libraries:

- numpy
- random
- math
- datetime
- matplotlib.pyplot
- csv

## Parameter description

In the veinSimulator simulation parameters are changed by modifying the source code in the Simulator.py file.

- drawPlot - Set True to enable the plot drawing. Set False otherwise
- transmissionTime - time of the nano nodes' transmission in us
- simulationQuantity - quantity of the simulations for each number of the nano nodes in the bloodstream
- veinLength - vein length in mm
- bloodVolume - blood volume in the bloodstream in mm^3
- veinDiameter - vein diameter in mm
- latencyVariation - Maximum latency for the nano nodes in the asynchronous mode in 10 ms. Set 0 for the network synchronous mode
- router range - range of the router in mm

## License

Copyright 2022 [@KrzysztofSkos](https://github.com/KrzysztofSkos)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
