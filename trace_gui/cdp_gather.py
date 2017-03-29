import su
import fnmatch
import numpy as np
import cdp_gather
import scaler

class CDP(object):
    #Loads first CDP for default
    def __init__(self, filepath, cdp_index=1):
        if(fnmatch.fnmatch(filepath, '*.su')):
            self.filepath = filepath
            self.cdp_index = cdp_index
            self.loadSU()
            self.loadCDP(self.cdp_index)

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
        self.ncdps = len(np.unique(self.data['cdp']))

    def loadCDP(self, cdp_index = 1):
        #Collecting traces from a specific cdp
        if(cdp_index <= self.ncdps and cdp_index > 0):
            traces = []
            traces_index = []
            for i in range(0, len(self.data)):
                if(self.data['cdp'][i] == cdp_index):
                    traces.append(self.data['trace'][i])
                    traces_index.append(i)

            self.traces = traces
            self.traces_index = traces_index
        else:
            raise TypeError("Cdp index not existent in file")
        return self

    def scale_traces(self, perc):
        #difference between two offsets in a CDP
        #TO DO
        #funcao bugada
        dx = np.abs(self.data['offset'][self.traces_index[0]] - self.data['offset'][self.traces_index[1]])
        self.traces = scaler.scale_data_map(self.traces, perc, dx)
        return self
