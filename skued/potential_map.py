# -*- coding: utf-8 -*-
"""
3D Reconstruction of scattering potential
=========================================
"""

import numpy as np

from . import bounded_reflections, powdersim, structure_factor

# TODO: test
#       Not exporting this function until tests are written
def potential_map(q, I, crystal, mesh):
    """ 
    Compute the electrostatic potential from powder diffraction data.
    
    Parameters
    ----------
    q, I : ndarray, shapes (N,)
        Scattering vector norm and intensity data
    crystal : Crystal instance

    mesh : 3-tuple ndarrays, ndim 2 or ndim 3
        Real-space mesh over which to calculate the scattering map.
        Format should be similar to the output of numpy.meshgrid. 

    Returns
    -------
    out : ndarray, ndim 2

    Raises
    ------
    ValueError
        If intensity data is not strictly positive.

    Notes
    -----
    To compute the scattering map from a difference of intensities, note that scattering 
    maps are linear in structure factor norm. Thus, to get the map of difference data I1 - I2:
        I = np.square(np.sqrt(I1) - np.sqrt(I2))
    
    References
    ----------
    TODO
    """
    if np.any(I < 0):
        raise ValueError('Diffracted intensity cannot physically be negative.')
    
    # We want to support 2D and 3D meshes, therefore 
    # expand mesh until 4D (last dim is for loop over reflections)
    # Extra dimensions will be squeezed out later
    xx, yy, zz = mesh
    while xx.ndim < 4:
        xx, yy, zz = np.expand_dims(xx, 3), np.expand_dims(yy, 3), np.expand_dims(zz, 3)

    # Prepare reflections
    # G is reshaped so that it is perpendicular to xx, yy, zz to enables broadcasting
    hs, ks, ls = bounded_reflections(crystal, q.max())
    SF = structure_factor(crystal, hs, ks, ls )

    # Extract structure factor with correction factors
    # Diffracted intensities add up linearly (NOT structure factors)
    qx, qy, qz = crystal.scattering_vector(hs, ks, ls)
    qx, qy, qz = qx.reshape((1,1,1,-1)), qy.reshape((1,1,1,-1)), qz.reshape((1,1,1,-1))
    SF = SF.reshape((1,1,1,-1))
    q_theo = np.squeeze(np.sqrt(qx**2 + qy**2 + qz**2))
    theo_I = powdersim(crystal, q_theo)
    peak_mult_corr = np.abs(SF)**2/theo_I
    exp_SF = np.sqrt(np.interp(q_theo, s, I)) * peak_mult_corr

    # Squeeze out extra dimensions (e.g. if mesh was 2D)
    potential_map = np.sum(exp_SF * np.real(np.exp(1j * np.angle(SF))) * np.cos(xx*qx + yy*qy + zz*qz), axis = 3)
    return np.squeeze(potential_map)