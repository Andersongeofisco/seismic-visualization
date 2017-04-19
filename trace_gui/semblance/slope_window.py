#TO DO

# import cdp_gather
# from math import pi
# import numpy as np
# from math import floor
# from math import ceil
# import time

class slope(object):
    def __init__(self, resolution, trace_ref, cdp_obj, L):
        #Depends if its a sea or land sonar
        self.cdp_obj = cdp_obj
        self.max_slope = 1.0/1200
        self.resolution = resolution #arbitraly 64 according to Billete thesis
        self.trace_ref = trace_ref
        self.trace_ref_pos = cdp_obj.data['offset'][cdp_obj.traces_index[trace_ref]]
        self.dt = cdp_obj.interval
        self.nsamples = cdp_obj.nsamples

    #L: window of the hamming function defined by Billete
    #px: slope value
    #traces_values: list of trace values in the time tau
    #wj weight of trace according to the hamming function
    #trj value of a sample for a given time t for a given trace
    def local_slant_slack(self, L, px, tau, traces, exp):
        x0 = self.trace_ref_pos
        lss = 0
        #number of neighbours
        neigh = 0
        for j,trace in enumerate(traces):
            trj_index = self.cdp_obj.traces_index[j]
            xj =  self.cdp_obj.data['offset'][trj_index]
            if (np.abs(xj - x0) <= L):
                wj = self.hamming_function(xj - x0 , L)
                #not so sure
                t = abs(tau + px*(xj - x0))
                # t = tau + px*(xj - x0)
                # if t >= 0:
                #if t is in the middle of two samples in the trace
                #interpolate between the two nearest sample values
                if(floor(t/self.dt) >= 0 and ceil(t/self.dt) <= self.nsamples - 1):
                    trj = (trace[floor(t/self.dt)] + trace[ceil(t/self.dt)])/2
                    lss = lss + pow(wj*trj, exp)
                    neigh += 1
        return {'lss': lss, 'neigh': neigh}

    def hamming_function(self, x, L):
        return 0.5 + 0.5*np.cos((pi*x)/L)

    def coherence(self):
        #X-axis
        dp =  (1/self.resolution)*2*self.max_slope
        slope_scale = np.arange(-self.max_slope, self.max_slope, dp)
        #Y-axis
        #Time vector
        y = np.linspace(0, self.cdp_obj.nsamples*self.cdp_obj.interval, self.cdp_obj.nsamples)
        #Coherence matrix
        semblance_window = np.zeros((len(y), len(slope_scale)))

        start = time.time()
        for i, t in enumerate(y):
            for j, p in enumerate(slope_scale):
                lss = self.local_slant_slack(100, p, t, self.cdp_obj.traces, 2)
                neigh = lss['neigh']
                sum_square = lss['lss']
                lss = self.local_slant_slack(100, p, t, self.cdp_obj.traces, 1)
                square_sum = pow(lss['lss'],2)

                #marfurt semblance
                if(neigh):
                    semblance_window[i][j] = (1/neigh)*(square_sum/sum_square)
                else:
                    semblance_window[i][j] = 0

        print("Calculo do semblance demorou ", start - time.time())
        return semblance_window

        #uma duvida: pegar o valor do sample da fita ou somado ao offset?
        #com L = 100m, aproxidamente 4 vizinhos se o dx for 25?
        #TO DO: check why 11 neighbours
