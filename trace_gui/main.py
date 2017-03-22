import pyqtgraph as pg
from pyqtgraph import QtGui
from pyqtgraph import QtCore
import numpy as np
import cdp_gather as cdp


## Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])

## Define a top-level widget to hold everything
w = QtGui.QWidget()

## Create some widgets to be placed inside
btn = QtGui.QLabel('CDP index')
#text = QtGui.QLineEdit('enter text')
text = QtGui.QSpinBox()
listw = QtGui.QListWidget()

#Setting background and axis configuration
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
#Setting plotting line color

plot = pg.PlotWidget(parent=None)

#Modify widgets
#Procurar funcao de set between lines
plot_item = plot.getPlotItem()

#Plotting for a specific cdp
cdp_item = cdp.CDP("traces.su", 123).scale_traces(90)
trace = cdp_item.traces[0]
offset = cdp_item.data['offset'][cdp_item.traces_index[0]]

y = np.linspace(0, cdp_item.nsamples*cdp_item.interval, cdp_item.nsamples)
x = trace + offset
plot_item.addItem(pg.PlotDataItem(x, y, pen=pg.mkPen('k', width=0.5)))


#PlotDataItem()

## Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout()
w.setLayout(layout)

## Add widgets to the layout in their proper positions
layout.addWidget(btn, 0, 0)   # button goes in upper-left
layout.addWidget(text, 1, 0)   # text edit goes in middle-left
layout.addWidget(listw, 2, 0)  # list widget goes in bottom-left
layout.addWidget(plot, 0, 1, 3, 1)  # plot goes on right side, spanning 3 rows

## Display the widget as a new window
w.show()

## Start the Qt event loop
app.exec_()
