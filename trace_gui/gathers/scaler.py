import numpy as np

def get_max_amplitude(traces, perc):
    sorted_array = np.sort(np.abs(traces), axis=None)
    tam = len(sorted_array)
    index = round((perc/100)*tam)
    max_amplitude = sorted_array[index - 1]

    return max_amplitude
#TO DO: divide the scale values by the RMS amplitude (square root of the average of the sum of the square or the trace values)
def scale_data(traces, perc, dx):
    #Correcting amplitudes for all data
    max_amplitude =  get_max_amplitude(traces, perc)
    new_data = []
    scale = dx/max_amplitude
    #scale = 0.05
    for trace in traces:
        corrected_data = np.array([x  if abs(x) <= max_amplitude else max_amplitude*np.sign(x) for x in trace])
        new_data.append(scale*corrected_data)

    return new_data

def scale_data_map(traces, perc, dx):
    #Correcting amplitudes for all data
    max_amplitude =  get_max_amplitude(traces, perc)
    new_data = []
    scale = dx/max_amplitude
    new_data = list(map(lambda trace : np.array([x  if abs(x) <= max_amplitude else max_amplitude*np.sign(x) for x in trace])*scale
                    , traces))
    return new_data
