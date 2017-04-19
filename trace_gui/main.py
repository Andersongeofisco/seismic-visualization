import pyqtgraph as pg
from pyqtgraph import QtGui
from pyqtgraph import QtCore
import numpy as np
import gathers.cdp_gather as cdp
from windows import cmpPlot

## Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])

## Define a top-level widget to hold everything
w = QtGui.QWidget()

#Setting background and axis configuration
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

cmp = cmpPlot.cmpPlot()


cdp_item = cdp.CDP("traces.su", 123)
offsets = cdp_item.getOffsets()
cmp.show_plot(cdp_item.index, cdp_item.nsamples, cdp_item.interval, offsets, cdp_item.scale_traces(99))

## Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout()
w.setLayout(layout)

## Add widgets to the layout in their proper positions
layout.addWidget(cmp.window, 1, 0)

## Display the widget as a new window
w.show()

## Start the Qt event loop
app.exec_()
