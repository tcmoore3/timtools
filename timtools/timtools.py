"""
timtools.py
Some functions I find myself rewriting frequently

Handles the primary functions
"""
import freud
import gsd.hoomd


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
    with gsd.open(filename, 'rb') as traj:
        N = traj[frame].particles.N
    return N
