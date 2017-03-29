import cdp_gather as cdp
import pyqtgraph as pg
from pyqtgraph import QtGui
from pyqtgraph import QtCore
import numpy as np
import time


class cdp_gui(object):
    def __init__(self):
        self.plot = pg.PlotWidget(parent=None)
        self.cdp_obj = cdp.CDP("traces.su", 123).scale_traces(90)
        self.spin = pg.SpinBox()
        self.spin_label = QtGui.QLabel('CDP')
        #Max e min cdps from tape
        self.spin.setRange(1, self.cdp_obj.ncdps)
        #Default value for visualization
        self.spin.setValue(self.cdp_obj.cdp_index)
        self.spin.setSingleStep(1)
        self.spin.sigValueChanged.connect(self.plot_cdp)


    def plot_cdp(self):

        plot_item = self.plot.getPlotItem()

        if plot_item:
            plot_item.clear()

        #Plotting for a specific cdp
        #first load cdp
        print(self.spin.value())
        self.cdp_obj.loadCDP(int(self.spin.value())).scale_traces(90)

        y = np.linspace(0, self.cdp_obj.nsamples*self.cdp_obj.interval, self.cdp_obj.nsamples)

        for i,trace in enumerate( self.cdp_obj.traces):
            offset =  self.cdp_obj.data['offset'][self.cdp_obj.traces_index[i]]
            x = trace + offset
            plot_item.addItem(pg.PlotDataItem(x, y, pen=pg.mkPen('k', width=0.5)))

        #print(start_time - time())
