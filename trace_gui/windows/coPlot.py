import pyqtgraph as pg
from pyqtgraph import QtGui
from pyqtgraph import QtCore
import numpy as np

class coPlot(object):
    def __init__(self):
        self.window = pg.PlotWidget(parent=None)
        self.pos = -1
        self.traces_items = {} #dict of trace item plots by position of trace

    def show_plot(self, off_pos, nsamples, interval, offsets, traces):
        if(off_pos is not self.pos):
            self.window.clear()
            self.pos = off_pos

            y = np.linspace(0, nsamples*interval, nsamples)
            for i, (trace, offset) in enumerate(zip(traces, offsets)):
                center = (offset + off_pos)
                x = trace + center
                item = pg.PlotDataItem(x, y, pen=pg.mkPen('k', width=0.5))
                self.traces_items[str(center)] = item
                self.window.addItem(item)
