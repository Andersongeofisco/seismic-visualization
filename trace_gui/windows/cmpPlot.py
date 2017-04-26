import pyqtgraph as pg
from pyqtgraph import QtGui
from pyqtgraph import QtCore
import numpy as np

class cmpPlot(object):
    def __init__(self):
        self.window = pg.PlotWidget(parent=None)
        self.cdp_index = -1
        self.traces_items = {} #dict of trace item plots by position of trace

    def show_plot(self, cdp_index, nsamples, interval, offsets, traces):
        if(cdp_index is not self.cdp_index):
            self.window.clear()
            self.cdp_index = cdp_index

            y = np.linspace(0, nsamples*interval, nsamples)
            for i, (trace, offset) in enumerate(zip(traces, offsets)):
                x = trace + offset
                item = pg.PlotDataItem(x, y, pen=pg.mkPen('k', width=0.5))
                self.traces_items[str(offset)] = item
                self.window.addItem(item)
