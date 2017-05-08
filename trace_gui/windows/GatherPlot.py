from pyqtgraph import PlotWidget
from windows.PlotTraceItem import PlotTraceItem
from pyqtgraph import PlotCurveItem
import pyqtgraph as pg
import numpy as np
from copy import deepcopy

class GatherPlotWidget(PlotWidget):
    def __init__(self, gather, refTrace = None, drawRef = False):
        super(GatherPlotWidget, self).__init__(parent=None)
        self.gather = gather
        self.refTrace = refTrace
        self.refLine = None
        self.drawRef = drawRef
        #Plot trace gathers
        self.plotGather()

        if(self.drawRef):
            self.refLine = self.drawRefLine()

    def drawRefLine(self):
        if(self.drawRef):
            refParams = self.refTrace.traceParams
            y = np.linspace(0, self.gather.nsamples*self.gather.interval,  self.gather.nsamples)
            x = np.tile(refParams['posX'], len(y))

            if(self.refLine is None):
                self.refLine = PlotCurveItem(x, y,  pen=pg.mkPen('r', width=2))
            else:
                self.refLine.setData(x, y)
            self.addItem(self.refLine)
        else:
            self.refLine = None

        return self.refLine

    def traceClicked(self, trace):
        self.refTrace = trace
        print(trace.traceParams)
        self.drawRefLine()

    #Wiggle plot
    def plotGather(self):
        traces =  self.gather.scaleTraces(99)
        offsets = self.gather.getOffsets()
        indexes = self.gather.traces_index

        if(self.getPlotItem()):
            self.getPlotItem().clear()

        y = np.linspace(0, self.gather.nsamples*self.gather.interval,  self.gather.nsamples)
        self.setYRange(np.min(y), np.max(y))

        for trace, offset, index in zip(traces, offsets, indexes):
            trace[0] = 0
            trace[-1] = 0
            #Zero crossings
            crossing = np.where(np.diff(np.signbit(trace)))[0]
            #Interpolate
            x1=  trace[crossing]
            x2 =  trace[crossing+1]
            y1 = y[crossing]
            y2 = y[crossing+1]
            m = (y2 - y1)/(x2-x1)
            c = y1 - m*x1
            xTemp = np.hstack([trace, np.zeros_like(c)])
            yTemp = np.hstack([y, c])
            #Resort the data
            order = np.argsort(yTemp)
            #New data with zero crossings in correct positions
            trace = xTemp[order]
            yTrace = yTemp[order]

            negCurve = deepcopy(trace)
            posCurve = deepcopy(trace)
            posCurve[posCurve < 0] = 0
            negCurve[negCurve > 0] = 0

            posItem = PlotTraceItem(posCurve + offset, yTrace, self.gather.getTraceParams(index))
            negItem = PlotTraceItem(negCurve + offset, yTrace, self.gather.getTraceParams(index))
            #Fill only positives of curve
            posItem.setFillLevel(offset)
            posItem.setBrush(pg.mkBrush(0,0,0))
            offItem = PlotCurveItem(np.tile(offset, len(y)), y, pen=pg.mkPen('w', width=1))
            posItem.sigClicked.connect(self.traceClicked)
            negItem.sigClicked.connect(self.traceClicked)
            self.addItem(posItem)
            self.addItem(negItem)
            self.addItem(offItem)

        if(self.refTrace is None):
            self.refTrace = posItem
