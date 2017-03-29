import pyqtgraph as pg
from pyqtgraph import QtGui
from pyqtgraph import QtCore
import numpy as np
import cdp_gather as cdp
import cdp_gui
import time

## Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])

## Define a top-level widget to hold everything
w = QtGui.QWidget()

## Create some widgets to be placed inside
# cdp_index_text = QtGui.QLabel('CDP')
# cdp_index_spin = QtGui.QSpinBox()
# cdp_index_spin.setValue(95)

cdp_scale_text = QtGui.QLabel('Perc')
cdp_scale_spin = QtGui.QSpinBox().setValue(90)

#Setting background and axis configuration
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

plot2 = pg.PlotWidget(parent=None)
#Modify widgets
#Procurar funcao de set between lines


cdp_window = cdp_gui.cdp_gui()
cdp_index_text = cdp_window.spin_label
cdp_index_spin = cdp_window.spin
cdp_window.plot_cdp()

# cdp_window2 = cdp_gui.cdp_gui(cdp_obj2, plot2)
# #cdp_index_text2 = cdp_window.spin_label
# #cdp_index_spin2 = cdp_window.spin
# cdp_window2.plot_cdp()

#PlotDataItem()

## Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout()
w.setLayout(layout)

## Add widgets to the layout in their proper positions
layout.addWidget(cdp_index_text, 0, 0, 1, 1)
layout.addWidget(cdp_index_spin, 1, 0, 2, 2)
# layout.addWidget(cdp_scale_text, 0, 2, 1, 1)
# layout.addWidget(cdp_scale_spin, 1, 1, 1, 1)
layout.addWidget(cdp_window.plot, 2, 2, 20, 20)
layout.addWidget(plot2, 2, 22, 20, 20)


## Display the widget as a new window
w.show()

## Start the Qt event loop
app.exec_()
