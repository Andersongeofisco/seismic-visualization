import pyqtgraph as pg
from pyqtgraph import QtGui
from pyqtgraph import QtCore
import numpy as np
from gathers.Gather import Gather
from windows.GatherPlot import GatherPlotWidget
from windows.controller import gatherCoord

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

traceRef = cs_item.getTraceParams(0)
print("before")
print(co_item.index)
control = gatherCoord(cs_item, co_item, traceRef)
print("after")
print(co_item.index)

# cmp = GatherPlotWidget(cdp_item)
cs_p = GatherPlotWidget(cs_item)
# cr_p = GatherPlotWidget(cr_item)
co_p = GatherPlotWidget(co_item)

# cmp.plotGather()
cs_p.plotGather()
# cr_p.plotGather()
co_p.plotGather()

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
