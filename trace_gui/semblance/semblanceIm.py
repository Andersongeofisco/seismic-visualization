#TO DO

# import cdp_gather as cdp
# import pyqtgraph as pg
# from pyqtgraph import QtGui
# from pyqtgraph import QtCore
# import numpy as np
# import slope_window as slope


#Receives a CDP class and an ImageView to plot semblance
def plot_semb(cdp_obj, window):
    pos = np.array([0.0,0.25, 0.5, 0.75, 1.0])
    #Choose color points
    color = np.array([[0,0,255],[0,255,255], [0,255,0], [255,255,0], [255,0,0]],dtype=np.ubyte)
    cm = pg.ColorMap(pos, color)
    #Calculate window semblance
    semblance_window = slope.slope(64,24, cdp_obj, 100).coherence()
    #Plot image
    window.setImage(np.array(semblance_window).T)
    #Color image
    window.plot_semblance.setColorMap(cm)
