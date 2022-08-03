"""
Module to analyze and post-process particles from ASPECT
"""
import os
import numpy as np
from scipy.spatial import KDTree
from joblib import Parallel,delayed
from tqdm import tqdm

def nearest_neighbor_KDTree(position,positions):
    """
    Find nearest neighbor of a particle using X,Y,Z positions.

    Uses KDTree function from SciPy
    """
    # Get nearest neighbor from KDTree
    distance,index = KDTree(positions).query(position)

    return(index)

def run_scalar_forward(source_mesh,future_meshes,field,interpolate=True,
                        processes=os.cpu_count()-6):
    """
    Apply scalar values on particles to same particles in future meshes
    """
    # Get ids of old particles
    old_particles = source_mesh['id']

    # Get scalars corresponding to those ids
    old_scalars = source_mesh[field]

    # Get positions for those ids
    old_positions = source_mesh.points

    for mesh in tqdm(future_meshes):
        
        # Get new particle ids
        new_particles = mesh['id']
        new_positions = mesh.points

        # Loop through new particles
        new_scalars = Parallel(n_jobs=processes,require='sharedmem')(
            delayed(get_previous_scalar)(particle,new_positions[k],old_particles,old_scalars,
                old_positions, interpolate=interpolate) 
                for k,particle in enumerate(new_particles)
            ) 

        mesh[field] = new_scalars

        old_particles = new_particles
        old_scalars = np.array(new_scalars)
        old_positions = new_positions

    return(future_meshes)

def get_previous_scalar(particle,position,old_particles,old_scalars,
    old_positions,interpolate=False):
    """
    Get scalar value from previous timestep
    """
    # Try to get scalar from particles
    scalar = old_scalars[particle==old_particles]
    
    # Check if scalar actually exists
    if (scalar.size == 0) & (interpolate == False):
        new_scalar = np.nan
    
    elif (scalar.size == 0) & (interpolate == True):
        
        # Find index of nearest neighbor
        nn_index = nearest_neighbor_KDTree(position,old_positions)
        
        # Assign scalar using nearest neighbor index
        new_scalar = float(old_scalars[nn_index])

    elif (scalar.size == 1):
        new_scalar = float(scalar)

    else:
        # Skip if duplicates of particle id
        new_scalar = np.nan

    return(new_scalar)        




