"""
Module for generating appropriate flow law parameters
"""

class FlowLaw:
    def __init__(self,material,source,wetness,creep,COH=1000):
        self.material = material
        self.source = source
        self.wetness = wetness
        self.creep = creep
        self.COH = COH

        return

    def get_published(self):
        props = (self.material,self.source,self.wetness,self.creep)

        if props == ('olivine','hirth','dry','dislocation'):
            self.A_pub = 1.1e5 # s^-1 MPa^-n um^m COH^-r
            self.n = 3.5
            self.m = 0
            self.r = 0
            self.E_pub = 530 # kJ/mol
            self.V_pub = 18 # 10^-6 m^3/mol - note this is actually a range

        elif props == ('olivine','hirth','dry','diffusion'):
            self.A_pub = 1.5e9 # s^-1 MPa^-n um^m COH^-r
            self.n = 1
            self.m = 3
            self.r = 0
            self.E_pub = 375 # kJ/mol
            self.V_pub = 4 # 10^-6 m^3/mol - note this is actually a range
        
        elif props == ('olivine','hirth','wet','dislocation'):
            self.A_pub = 1600 # s^-1 MPa^-n um^m COH^-r
            self.n = 3.5
            self.m = 0
            self.r = 1.2
            self.E_pub = 520 # kJ/mol
            self.V_pub = 22 # 10^-6 m^3/mol
        
        elif props == ('olivine','hirth','wet','diffusion'):
            self.A_pub = 2.5e7 # s^-1 MPa^-n um^m COH^-r
            self.n = 1
            self.m = 3
            self.r = 1 # actually a range
            self.E_pub = 375 # kJ/mol
            self.V_pub = 4 # 10^-6 m^3/mol

        values = (self.A_pub,self.n,self.m,self.r,self.E_pub,self.V_pub)
        return(values)

    def convert2SI(self):
        """Convert published values to SI units"""
        self.A_SI = self.A_pub * 1e6**-self.n * 1e-6**self.m * self.COH**-self.r # s^-1 Pa^-n m^m COH^-r

        self.E_SI = self.E_pub * 1e3 # j/mol

        self.V_SI = self.V_pub * 1e-6 # m^3/mol

        return(self.A_SI,self.E_SI,self.V_SI)

    def scaleA_gerya(self,experiment='axial',function='strain rate'):
        """Scale prefactor (A) according to the appropriate experiment, following Gerya textbook"""
        if experiment=='axial':
            if function=='strain rate':
                factor = (2**(self.n-1)*3**((self.n+1)/(2*self.n)))
            elif function=='stress':
                factor = (3**((self.n+1)/2))
        
        elif experiment=='simple shear':
            if function=='strain rate':
                factor = (2**((2*self.n-1)/self.n))
            elif function=='stress':
                factor = 2**self.n

        self.A_scaled = self.A_SI*factor

        return(self.A_scaled)

    def scaleA_dannberg(self):
        """Scale prefactor (A) according to Dannberg et al., 2017"""

        factor = 3**((self.n+1)/2)/2

        self.A_scaled = self.A_SI*factor
        
        return(self.A_scaled)
