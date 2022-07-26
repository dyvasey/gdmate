"""
Module for flow law calculations
"""
import numpy as np

def get_published(mineral,source,creep,dryness):
    """
    Get published values for flow law.
    """
    props = (mineral,source,creep,dryness)

    if props == ('olivine','hirth','dislocation','dry'):
        A = 1.1e5 # MPa^-n-r um^m_diff
        n = 3.5
        m_diff = 0
        r = 0
        E = 530 # kJ/mol

        # V taken from Table 2 but is variable
        V = 18 # 10^-6 m^3/mol

    elif props == ('olivine','hirth','dislocation','wet'):
        # Used values for constant COH of 1000 H/10^6Si
        A = 90 # MPa^-n-r um^m_diff
        n = 3.5
        m_diff = 0
        r = 1.2
        E = 480 # kJ/mol
        V = 11 # 10^-6 m^3/mol

    elif props == ('olivine','hirth','diffusion','dry'):
        A = 1.5e9 # MPa^-n-r um^m_diff
        n = 1
        m_diff = 3
        r = 0
        E = 375 #kJ/mol

        # Lower end of a range from 2-10
        V = 2 # 10^-6 m^3/mol

    elif props == ('olivine','hirth','diffusion','wet'):
        # Used values for constant COH of 1000 H/10^6Si
        A = 1.0e6 # MPa^-n-r um^m_diff
        n = 1
        m_diff = 3
        r = 1
        E = 335 # kJ/mol
        V = 4 # 10^-6 m^3/mol

    elif props == ('quartzite','gleason','dislocation','wet'):
        # Water fugacity not included in units so not used for conversion
        A = 1.1e-4 # MPa^-n s^-1 um^m_diff
        n = 4
        m_diff = 0
        r = 0 # Not considered
        E = 223 # kJ/mol
        V = 0 # 10^-6 m^3/mol
    
    return(A,n,m_diff,r,E,V)
        
def convert2SI(values):
    """
    Convert published flow law values to SI units.
    
    Assumes units follow Hirth03
    """

    A_pub = values[0]
    n = values[1]
    m_diff = values[2]
    r = values[3]
    E_pub = values[4]
    V_pub = values[5]

    A_SI = A_pub * 1e6**(-n-r) * 1e-6**(m_diff) # s^-1 Pa^-n-r m^m_diff
    E_SI = E_pub * 1000 # J/mol
    V_SI = V_pub * 1e-6 # m^3/mol

    values_SI = (A_SI,n,m_diff,r,E_SI,V_SI)

    return(values_SI)

def scaleA(A_SI,n):
    """
    Scale A from uniaxial experiments for ASPECT.

    Implemented in Danneburg et al., 2017
    """
    A_scaled = 2**(n-1) * 3**((n+1)/2) * A_SI

    return(A_scaled)

def get_flow_law_parameters(mineral,source,creep,dryness):

    values = get_published(mineral,source,creep,dryness)
    values_str = ['{:0.2e}'.format(x) for x in values]

    print('Published Values:')
    print('A - prefactor (MPa^-n-r um^m_diff: ',values_str[0])
    print('n - stress exponent: ',values_str[1])
    print('m_diff - grain size exponent: ',values_str[2])
    print('r - fugacity exponent: ',values_str[3])
    print('E - activation energy (kJ/mol)',values_str[4])
    print('V - activation volume (10^-6 m^3/mol)',values_str[5])

    converted = convert2SI(values)
    converted_str = ['{:0.2e}'.format(x) for x in converted]

    print('\nConverted to SI Units:')
    print('A (Pa^-n-r m^m_diff): ',converted_str[0])
    print('E - activation energy (J/mol): ',converted_str[4])
    print('V - activation volume (m^3/mol): ',converted_str[5])

    A_scaled = scaleA(converted[0],converted[1])
    A_scaled_str = '{:0.2e}'.format(A_scaled)

    print('\nScaled A for ASPECT:')
    print('A scaled (Pa^-n-r m^m_diff): ',A_scaled_str)

    return(A_scaled,values[1],values[2],values[3],converted[4],
            converted[5])