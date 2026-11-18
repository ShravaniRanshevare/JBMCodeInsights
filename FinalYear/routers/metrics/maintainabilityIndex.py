import math

class MaintainabilityIndex:
    def __init__(self,hal_vol,CC,LOC):
        self.vol = hal_vol
        self.cc = CC
        self.loc = LOC
    
    def getIndex(self):
        return (171 - 5.2*math.log(self.vol) - 0.23*(self.cc) - 16.2*math.log(self.loc))
    