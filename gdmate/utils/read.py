"""
Module for reading data from model outputs
"""
import pyvista as pv

def pvread(file,**kwargs):
    """ Wrapper for pyvista.read function """
    mesh = pv.read(file,**kwargs)
    return(mesh)