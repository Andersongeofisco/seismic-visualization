from pyqtgraph import PlotWidget
from windows.PlotTraceItem import PlotTraceItem
import numpy as np

#Plotar traços do gather
#Plotar linha vermelha de referência

class GatherPlotWidget(PlotWidget):
    def __init__(self, gather, refTrace = None):
        super(GatherPlotWidget, self).__init__(parent=None)
        self.gather = gather
        self.refTrace = refTrace

    def plotGather(self):
        traces =  self.gather.scaleTraces(99)
        offsets = self.gather.getOffsets()
        indexes = self.gather.traces_index

        y = np.linspace(0, self.gather.nsamples*self.gather.interval,  self.gather.nsamples)
        for trace, offset, index in zip(traces, offsets, indexes):
            x = trace + offset
            tracePlot = PlotTraceItem(x, y, self.gather.getTraceParams(index))
            #add callback to item
            self.addItem(tracePlot)




    #def plotRefTrace():
