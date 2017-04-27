import suTools.su as su
import fnmatch
import numpy as np
from dataScaler import scaler

class CR(object):
    #Load first receiver by default
    def __init__(self, filepath, index=1):
        if(fnmatch.fnmatch(filepath, '*.su')):
            self.filepath = filepath
            self.index = index
            self.loadSU()
            self.loadCS(self.index)
            #TO-DO
            # self.dx =  np.abs(self.data['offset'][self.traces_index[0]] - self.data['offset'][self.traces_index[1]])
            self.dx=20
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
        self.ncr = len(np.unique(self.data['gx']))
        self.receivers = dict(enumerate(np.unique(self.data['gx'])))

    def loadCS(self, index = 1):
        self.index = index
        #Collecting traces from a specific cdp
        if(index <= self.ncr and index > 0):
            traces = []
            traces_index = []
            for i in range(0, len(self.data)):
                if(self.data['gx'][i] == self.getRecPos()):
                    traces.append(self.data['trace'][i])
                    traces_index.append(i)

            self.traces = traces
            self.traces_index = traces_index
        else:
            print(index)
            raise TypeError("Shot not existent in file")
        return self

    def getRecPos(self):
        return self.receivers[self.index-1]

    def getOffsets(self):
        offsets = []
        for index in self.traces_index:
            offsets.append(self.data['offset'][index])

        return offsets

    def scale_traces(self, perc):
        #difference between two offsets in a CDP
        #TO-DO
        #funcao bugada
        return scaler.scale_data_map(self.traces, perc, self.dx)
