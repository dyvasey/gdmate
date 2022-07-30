"""
Module to analyze and post-process particles from ASPECT
"""
import numpy as np
from numba import jit
from scipy.spatial import KDTree

def nearest_neighbor_KDTree(id,positions):
    """
    Find nearest neighbor of a particle using X,Y,Z positions.

    Uses KDTree function from SciPy
    """
    # Remove the particle from possible nearest neighbors
    # so it doesn't find itself
    mask = np.ones(len(positions),dtype=bool)
    mask[id] = False
    other_positions = positions[mask]
    
    # Get nearest neighbor from KDTree
    distance,index = KDTree(other_positions).query(positions[id])

    # Get position of the nearest neighbor
    nn_position = other_positions[index]

    # Find original index of the nearest neighbor
    nn = int(np.where(np.all(positions==nn_position,axis=1))[0])

    return(nn)

@jit
def nearest_neighbor_numpy(id,positions):
    """
    Find nearest neighbor of a particle using X,Y,Z positions.

    Uses pure Numpy to allow optimization with Numba
    """
    # Get position of particle
    pos = positions[id]
    
    # Remove the particle from possible nearest neighbors
    # so it doesn't find itself
    mask = np.empty(len(positions),dtype=np.bool_)
    mask[id] = False
    other_positions = positions[mask]

    # Calculate distances

    distances = np.sqrt(
        (pos[0]-other_positions[:,0])**2 + 
        (pos[1]-other_positions[:,1])**2 +
        (pos[2]-other_positions[:,2])**2
        )

    # Get index of the minimum distance
    index = np.argmin(distances)

    print(np.min(distances))
    # Get position of the nearest neighbor
    nn_position = other_positions[index]

    # Find original index of the nearest neighbor
    for x in range(len(positions)):
        if np.all(positions[x,0:3]==nn_position):
            nn=int(x)

    return(nn)

def run_scalar_forward(source_mesh,future_meshes,field):
    """
    Apply scalar values on particles to same particles in future meshes
    """
    source_particles = source_mesh.points

    for mesh in future_meshes:
        mesh_particles
