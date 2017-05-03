import pyqtgraph as pg
from pyqtgraph import PlotDataItem
import numpy as np

class PlotTraceItem(PlotDataItem):
    def __init__(self, xData, yData, traceParams):
        super(PlotTraceItem, self).__init__(xData, yData, pen=pg.mkPen('k', width=0.5))
        #gx, sx, offset e cdp
        self.traceParams = traceParams
