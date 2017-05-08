import pyqtgraph as pg
import numpy as np
from pyqtgraph import QtGui
from gathers.Gather import Gather
from windows.GatherPlot import GatherPlotWidget
from windows.controller import gatherCoord
from windows.PlotTraceItem import PlotTraceItem


## Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])

## Define a top-level widget to hold everything
w = QtGui.QWidget()

#Setting background and axis configuration
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

#cdp_item = Gather("data/traces_cdp.su", 20, "cdp", 50)
cs_item = Gather("data/traces_cs.su", 20,"sx", 0)
#cr_item = Gather("data/traces_cr.su", 20,"gx", 50)
co_item = Gather("data/traces_co.su", 10, "offset", 40)

#Initialize reference trace as the first trace available in gather
traceRef = cs_item.getTraceParams(0)
control = gatherCoord(cs_item, co_item, traceRef)

# cmp = GatherPlotWidget(cdp_item)
cs_p = GatherPlotWidget(cs_item, drawRef = True)
# cr_p = GatherPlotWidget(cr_item)
co_p = GatherPlotWidget(co_item)

## Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout()
w.setLayout(layout)

## Add widgets to the layout in their proper positions
# layout.addWidget(cmp, 1, 0)
layout.addWidget(cs_p, 0, 0)
# layout.addWidget(cr_p, 0, 0)
layout.addWidget(co_p, 1, 0)

## Display the widget as a new window
w.show()

## Start the Qt event loop
app.exec_()
