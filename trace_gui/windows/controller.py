
class gatherCoord(object):
    def __init__(self, firstGather, secGather, refTrace):
        self.firstGather = firstGather
        self.secGather = secGather
        self.loadGroup(refTrace)
    #Load gathers according to a reference trace from the first gather
    def loadGroup(self, refTrace):
        #MUDAR
        print(refTrace)
        key = refTrace[self.secGather.type]
        #Load in second gather traces according to the refTrace gather parameter
        #refTrace comes from firstGather
        groupIndex = self.secGather.getIndex(self.secGather.type, key)
        #Load group in second gather
        self.secGather.loadGather(groupIndex)
