import pyqtgraph as pg
from pyqtgraph import PlotCurveItem
import numpy as np
from signal import signal

class PlotTraceItem(PlotCurveItem):

    def __init__(self, xData, yData, traceParams):
        super(PlotTraceItem, self).__init__(xData, yData, pen=pg.mkPen('k', width=1),  clickable=True)
        #gx, sx, offset e cdp
        self.traceParams = traceParams
