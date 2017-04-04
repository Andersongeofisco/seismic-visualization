import cdp_gather as cdp
import pyqtgraph as pg
from pyqtgraph import QtGui
from pyqtgraph import QtCore
import numpy as np
import time
import slope_window as slope


class cdp_gui(object):
    def __init__(self):
        self.plot_traces = pg.PlotWidget(parent=None)
        self.plot_semblance = pg.ImageView(parent=None)
        self.cdp_obj = cdp.CDP("traces.su", 123)
        self.spin = pg.SpinBox()
        self.spin_label = QtGui.QLabel('CDP')
        #Max e min cdps from tape
        self.spin.setRange(1, self.cdp_obj.ncdps)
        #Default value for visualization
        self.spin.setValue(self.cdp_obj.cdp_index)
        self.spin.setSingleStep(1)
        self.spin.sigValueChanged.connect(self.plot_cdp)
        self.trace_pick_index = 24


    def plot_cdp(self):

        plot_item = self.plot_traces.getPlotItem()

        if plot_item:
            plot_item.clear()

        #Plotting for a specific cdp
        #first load cdp
        print(self.spin.value())
        scaled_traces = self.cdp_obj.loadCDP(int(self.spin.value())).scale_traces(90)

        y = np.linspace(0, self.cdp_obj.nsamples*self.cdp_obj.interval, self.cdp_obj.nsamples)

        for i,trace in enumerate(scaled_traces):
            offset =  self.cdp_obj.data['offset'][self.cdp_obj.traces_index[i]]
            x = trace + offset
            plot_item.addItem(pg.PlotDataItem(x, y, pen=pg.mkPen('k', width=0.5)))

    def plot_semb(self):
        pos = np.array([0.0,0.33,1.0])
        #Choose color points
        color = np.array([[0,0,255],[143,199,246], [250,250,210]],dtype=np.ubyte)
        cm = pg.ColorMap(pos, color)
        #Calculate window semblance
        semblance_window = slope.slope(64,24, self.cdp_obj, 100).coherence()
        #Plot image
        self.plot_semblance.setImage(np.array(semblance_window).T)
        #Color image
        self.plot_semblance.setColorMap(cm)
