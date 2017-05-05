from pyqtgraph import PlotWidget
from windows.PlotTraceItem import PlotTraceItem
from pyqtgraph import PlotCurveItem
import pyqtgraph as pg
import numpy as np

#Plotar traços do gather
#Plotar linha vermelha de referência

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

    def plotGather(self):
        traces =  self.gather.scaleTraces(99)
        offsets = self.gather.getOffsets()
        indexes = self.gather.traces_index

        if(self.getPlotItem()):
            self.getPlotItem().clear()

        y = np.linspace(0, self.gather.nsamples*self.gather.interval,  self.gather.nsamples)
        for trace, offset, index in zip(traces, offsets, indexes):
            x = trace + offset
            tracePlot = PlotTraceItem(x, y, self.gather.getTraceParams(index))
            tracePlot.sigClicked.connect(self.traceClicked)
            self.addItem(tracePlot)

        if(self.refTrace is None):
            self.refTrace = tracePlot


    #def plotRefTrace():
