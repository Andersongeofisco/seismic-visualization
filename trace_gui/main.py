import pyqtgraph as pg
from pyqtgraph import QtGui
from pyqtgraph import QtCore
import numpy as np
import gathers.cdp_gather as cdp
import gathers.cs_gather as cs
import gathers.cr_gather as cr
import gathers.co_gather as co
from windows import cmpPlot, csPlot, crPlot, coPlot
# from windows import csPlot

## Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])

## Define a top-level widget to hold everything
w = QtGui.QWidget()

#Setting background and axis configuration
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

cmp = cmpPlot.cmpPlot()
cs_p = csPlot.csPlot()
cr_p = crPlot.crPlot()
co_p = coPlot.coPlot()

cdp_item = cdp.CDP("data/traces_cdp.su", 123)
cs_item = cs.CS("data/traces_cs.su", 90)
cr_item = cr.CR("data/traces_cr.su", 90)
co_item = co.CO("data/traces_co.su", 1)
offsets = cdp_item.getOffsets()
offsets2 = cs_item.getOffsets()
offsets3 = cr_item.getOffsets()
offsets4 = co_item.getOffsets()

cmp.show_plot(cdp_item.index, cdp_item.nsamples, cdp_item.interval, offsets, cdp_item.scale_traces(99))
cs_p.show_plot(cs_item.getShotPos(), cs_item.nsamples, cs_item.interval, offsets2, cs_item.scale_traces(99))
cr_p.show_plot(cr_item.getRecPos(), cr_item.nsamples, cr_item.interval, offsets3, cr_item.scale_traces(99))
co_p.show_plot(co_item.getOffPos(), co_item.nsamples, co_item.interval, offsets4, co_item.scale_traces(99))


## Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout()
w.setLayout(layout)

## Add widgets to the layout in their proper positions
layout.addWidget(cmp.window, 1, 0)
layout.addWidget(cs_p.window, 0, 1)
layout.addWidget(cr_p.window, 0, 0)
layout.addWidget(co_p.window, 1,1)



## Display the widget as a new window
w.show()

## Start the Qt event loop
app.exec_()
