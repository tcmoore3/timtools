"""
timtools.py
Some functions I find myself rewriting frequently

Handles the primary functions
"""
import freud
import gsd.hoomd
import numpy as np


TTDEFAULTS = {
        'is2D': True,
        }


def _get_configuration(frame, is2D=TTDEFAULTS['is2D']):
    # get box and positions and orientations from frame
    box = frame.configuration.box
    if is2D:
        fbox = freud.box.Box(Lx=box[0], Ly=box[1], xy=box[3], is2D=True)
    else:
        fbox = freud.box.Box(Lx=box[0], Ly=box[1], Lz=box[2],
                xy=box[3], xz=box[4], yz=box[5])
    pos = frame.particles.position
    orientation = frame.particles.orientation
    return fbox, pos, orientation

def get_gsd_configurations(
        filename,
        start_frame=None,
        end_frame=None,
        frame_skip=None,
        is2D=TTDEFAULTS['is2D']):
    """Get box, positions, and orientations of particles in trajectory

    Parameters
    ----------
    filename : str
        The filename of the trajectory to open
    start_frame : int or None
        The frame to start on
    end_frame : int or None
        The frame to end on
    frame_skip : int or None
        The stride length
    is2D : bool, default=True
        Whether or not to return a 2D box

    Yields
    ------
    box : freud.box.Box
        The simulation box
    positions : np.ndarray, shape=(n, 3)
        The particle positions
    orientations : np.ndarray, shape=(n, 4)
        The particle orientations

    """
    traj_slice = slice(start_frame, end_frame, frame_skip)
    with gsd.hoomd.open(filename, 'rb') as traj:
        for frame in traj[traj_slice]:
            yield _get_configuration(frame)

def get_N_particles(filename, frame=0):
    """Get the number of particles in a specific frame of a trajectory

    Parameters
    ----------
    filename : str
        The filename
    frame : int, default=0

    Returns
    -------
    N : int
        The number of particles in the specified frame

    """
    with gsd.hoomd.open(filename, 'rb') as traj:
        N = traj[frame].particles.N
    return N

def get_largest_rcut(box):
    """Get the largest possible rcut for a given box

    This function simply finds the distances between each set of planes
    that define the simulation box, and returns the minimum of their halves.
    It is probably a good idea to set the r_cut value to something smaller
    than the value this function returns, like 0.95*get_largest_rcut(box).

    Args
    ----
    box : freud.box.Box
        The simulation box

    Returns
    -------
    max_rcut : float
        Half of the minimum plane-plane distance of the box faces

    """
    dist_x = box.Lx / np.sqrt(1.0 + box.xy**2 + (box.xy * box.yz - box.xz)**2)
    dist_y = box.Ly / np.sqrt(1.0 + box.yz**2)
    dist_z = box.Lz
    if box.is2D:
        return min(dist_x / 2, dist_y / 2)
    else:
        return min(dist_x/2, dist_y/2, dist_z/2)
