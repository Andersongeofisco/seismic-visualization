import su.reader as su
import fnmatch
import numpy as np
from dataScaler import scaler

class Gather(object):
    def __init__(self, filepath, dx, gatherType, index=0):
        if(fnmatch.fnmatch(filepath, '*.su')):
            self.filepath = filepath
            self.index = index
            #Gather types Available: Shot "sx" Receiver: "gx"
            #Midpoint: "cdp" Offset: "offset"
            self.type = gatherType
            #TO-DO: choose an appropriate distance between traces
            self.dx = dx
            self.loadSU()
            self.loadGather(self.index)
        else:
            raise TypeError("File type not supported. Please open a SU file.")
    #Reads data from file su or segy
    def loadSU(self):
        self.data = su.readSU(self.filepath)
        su_header = su.readSUheader(self.filepath)
        #Number of samples in a trace
        self.nsamples =  su_header['ns'][0]
        #Sample interval (microseconds) between samples in a trace for all traces
        self.interval = su_header['dt'][0]*pow(10,-6)
        #Number of traces with the same gather characteristic
        self.ngroups = len(np.unique(self.data[self.type]))
        self.groups  = dict(enumerate(np.unique(self.data[self.type])))

    def loadGather(self, index = 0):
        self.index = index
        if(self.type == "offset"):
            self.dx = self.getGroupPos()

        if(index < self.ngroups and index >= 0):
            traces = []
            traces_index = []
            for i in range(0, len(self.data)):
                if(self.data[self.type][i] ==  self.getGroupPos()):
                    traces.append(self.data['trace'][i])
                    traces_index.append(i)
            self.traces = traces
            self.traces_index = traces_index
        else:
            raise TypeError("Index not existent in gather")
        return self

    def getGroupPos(self):
        return self.groups[self.index]

    def getOffsets(self):
        off = self.getGroupPos()
        offsets = []
        for i,index in enumerate(self.traces_index):
            if(self.type == "offset"):
                offsets.append(i*self.data['offset'][index] + off)
            else:
                offsets.append(self.data['offset'][index])

        return offsets

    #Get group index in gather according to the parameter from the gather
    def getIndex(self,keyType, key):
        if(keyType is not self.type):
            raise TypeError("Wrong gather for this key type")
        else:
            #search for the group in gather data
            for index, value in self.groups.items():
                if(value == key):
                    return index
    #Get a parameter from a trace
    #Parameters: sx, gx, offset and cdp
    def getTraceParams(self, traceIndex):
        sx = self.data['sx'][traceIndex]
        gx = self.data['gx'][traceIndex]
        offset = self.data['offset'][traceIndex]
        cdp = self.data['cdp'][traceIndex]
        posX = self.getOffsets()[traceIndex]

        return {'sx': sx, 'gx': gx, 'offset': offset, 'cdp': cdp, 'posX': posX}


    def scaleTraces(self, perc):
        #difference between two offsets in a CDP
        #TO-DO
        #funcao bugada
        return scaler.scale_data_map(self.traces, perc, self.dx)
