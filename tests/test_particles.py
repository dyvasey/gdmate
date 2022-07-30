"""
Tests for particles module
"""
import pyvista as pv
import numpy as np

from gdmate.analysis_modules import particles

# Create simple Numpy array and Pyvista mesh
points = np.ones((int(1e6),3))*2
points[0,0:3] = [0,0,0]
points[2,0:3] = [0.5,0,0]

mesh = pv.PolyData(points).cast_to_unstructured_grid()

def test_nearest_neighbor_KDTree():
    """Test nearest_neighbor_KDTree function"""

    # Test using Numpy array
    id = 0

    nn = particles.nearest_neighbor_KDTree(id,points)

    assert nn == 2

    # Test using Pyvista points

    pv_points = mesh.points

    nn_pv = particles.nearest_neighbor_KDTree(id,pv_points)

    assert nn == 2

def test_nearest_neighbor_numpy():
    """Test nearest_neighbor_numpy function"""

    # Test using Numpy array
    id = 0

    nn = particles.nearest_neighbor_numpy(id,points)

    assert nn == 2

    # Test using Pyvista points

    pv_points = mesh.points

    nn_pv = particles.nearest_neighbor_numpy(id,pv_points)

    assert nn == 2

