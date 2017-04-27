import suTools.su as su
import fnmatch
import numpy as np
from dataScaler import scaler

class CO(object):
    #Load first receiver by default
    def __init__(self, filepath, index=1):
        if(fnmatch.fnmatch(filepath, '*.su')):
            self.filepath = filepath
            self.index = index
            self.loadSU()
            self.loadCO(self.index)
            #TO-DO

        else:
            raise TypeError("File type not supported")

    #Reads data from file su or segy
    def loadSU(self):
        self.data = su.readSU(self.filepath)
        su_header = su.readSUheader(self.filepath)

        #Number of samples in a trace
        self.nsamples =  su_header['ns'][0]
        #Sample interval (microseconds) between samples in a trace for all traces
        self.interval = su_header['dt'][0]*pow(10,-6)
        self.ncos = len(np.unique(self.data['offset']))
        self.offsets = dict(enumerate(np.unique(self.data['offset'])))

    def loadCO(self, index = 1):
        self.index = index
        self.dx = self.getOffPos()
        #Collecting traces from a specific cdp
        if(index <= self.ncos and index > 0):
            traces = []
            traces_index = []
            for i in range(0, len(self.data)):
                if(self.data['offset'][i] == self.dx):
                    traces.append(self.data['trace'][i])
                    traces_index.append(i)

            self.traces = traces
            print(len(traces))
            self.traces_index = traces_index
        else:
            print(index)
            raise TypeError("Offset not existent in file")
        return self

    def getOffPos(self):
        return self.offsets[self.index-1]

    def getOffsets(self):
        off = self.getOffPos()
        offsets = []
        for i, index in enumerate(self.traces_index):
            offsets.append(i*self.data['offset'][index] + off)

        return offsets

    def scale_traces(self, perc):
        #difference between two offsets in a CDP
        #TO-DO
        #funcao bugada
        return scaler.scale_data_map(self.traces, perc, self.dx)
