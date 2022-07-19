"""
Module for generating appropriate flow law parameters
"""

class FlowLaw:
    def __init__(self,material,source,wetness,creep):
        self.material = material
        self.source = source
        self.wetness = wetness
        self.creep = creep

        return

    def get_published(self):
        props = (self.material,self.source,self.wetness,self.creep)

        if props == ('olivine','hirth','dry','dislocation'):
            self.A_raw = 1.1e5 # s^-1 MPa^-n
            self.n = 3.5
            self.m = 0
            self.r = None
            self.E = 530 # kJ/mol
            self.V = 18 # 10^-6 m^3/mol - note this is actually a range

        elif props = ('olivine','hirth','dry','diffusion'):
            self.A_raw = 1.5e9 # s^-1 MPa^-n
            self.n = 1
            self.m = 3
            self.r = None
            self.E = 375 # kJ/mol
            self.V = 4 # 10^-6 m^3/mol - note this is actually a range
        
        elif props = ('olivine','hirth','wet','dislocation'):
            self.A_raw = 1600 # s^-1 MPa^-n
            self.n = 3.5
            self.m = 0
            self.r = 1.2
            self.E = 520 # kJ/mol
            self.V = 22 # 10^-6 m^3/mol
        
        elif props = 'olivine','hirth','wet','diffusion'):
            self.A_raw = 2.5e7 # s^-1 MPa^-n
            self.n = 1
            self.m = 3
            self.r = 1 # actually a range
            self.E = 375 # kJ/mol
            self.V = 4 # 10^-6 m^3/mol

        values = (self.A_raw,self.n,self.m,self.r,self.E,self.V)
        return(values)

        


def get_parameters(material,source,wetness='dry',creep='dislocation'):
    """
    Function to extract the appropriate published parameters
    """

    flow_law = FlowLaw(material,source,wetness,creep)

    return(flow_law)
