"""
Module for visualizing model results using Pyvista
"""
import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv

def pv_plot_2d(mesh,field,bounds=None,ax=None,colorbar=False,**kwargs):
    """
    Plot 2D mesh using Pyvista on a Matplotlib axes.

    Parameters:
        mesh : Pyvista mesh object
            A pyvista mesh object that contains geometrical representations
            of surface or volume data. The mesh may also have attributes,
            such as data values assigned to points, cells, or fields assigning
            various information to the mesh.
        field : float
            The name of the field contained within the Pyvista mesh object
            to plot. 
        bounds : list of floats or integers
            A list of four values that define the bounds by which to clip the 
            plot. Successively, the list of values define the minimum x,
            maximum x, minimum y, and maximum y bounds. (default: None)
            List of bounds (km) by which to clip the plot (default: None)
        ax : Matplotlib axes object 
            Matplotlib axis on which to plot the mesh (default: None)
        colorbar : Boolean 
            Boolean (True or False) for whether to include colorbar (default: False)

    Returns:
        ax : Matplotlib axes object
            Modified matplotlib axes object with the plotted mesh
    """
    
    if bounds is not None:
        # Add placeholder Z values to bounds
        bounds_3D = bounds + [0,0] # Add placeholder Z values to bounds
        # Clip mesh by bounds
        mesh = mesh.clip_box(bounds=bounds_3D,invert=False)
    
    # Set up Pyvista plotter offscreen
    pv.set_plot_theme("document")
    plotter = pv.Plotter(off_screen=True)
    
    # Add mesh to plotter
    plotter.add_mesh(mesh,scalars=field,**kwargs)
    
    # Set plotter to XY view
    plotter.view_xy()
    
    # Remove default colorbar if not enabled
    if colorbar==False:
        plotter.remove_scalar_bar()

    # Calculate Camera Position from Bounds
    bounds_array = np.array(bounds)
    xmag = float(abs(bounds_array[1] - bounds_array[0]))
    ymag = float(abs(bounds_array[3] - bounds_array[2]))
    aspect_ratio = ymag/xmag
    
    # Set a standard plotter window size
    plotter.window_size = (1024,int(1024*aspect_ratio))
    
    # Define the X/Y midpoints, and zoom level. The ideal zoom factor of 1.875 
    # was determined by trial and error
    xmid = xmag/2 + bounds_array[0]
    ymid = ymag/2 + bounds_array[2]
    zoom = xmag*aspect_ratio*1.875
    
    # Set camera settings for plotter window
    position = (xmid,ymid,zoom)
    focal_point = (xmid,ymid,0)
    viewup = (0,1,0)
    
    # Package camera settings as a list
    camera = [position,focal_point,viewup]
    
    # Assign the camera to the settings
    plotter.camera_position = camera
    
    # Create image
    img = plotter.screenshot(transparent_background=True)
    
    # Get current axes if none defined
    if ax is None:
        ax = plt.gca()
    
    # Plot using imshow
    ax.imshow(img,aspect='equal',extent=bounds)
    
    # Clear plot from memory
    plotter.clear()
    pv.close_all()
    
    return(ax)