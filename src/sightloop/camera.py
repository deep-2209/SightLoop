"""Camera geometry: recover 3D world positions from pixels + depth."""
import numpy as np


def pixel_to_world(view, proj, depth_buffer, u, v, width, height):
    """Map pixel (u, v) and its depth to a world (x, y, z).

    The inverse of (proj @ view) sends a clip-space point back to the world.
    Depth is used as the renderer's own clip-space z, never as meters.
    """
    proj_m = np.asarray(proj).reshape(4, 4, order="F")
    view_m = np.asarray(view).reshape(4, 4, order="F")
    inv = np.linalg.inv(proj_m @ view_m)

    ndc_x = 2.0 * u / width - 1.0
    ndc_y = 1.0 - 2.0 * v / height           # image row 0 is the TOP
    ndc_z = 2.0 * float(depth_buffer[v, u]) - 1.0   # depth[v, u], not [u, v]

    clip = np.array([ndc_x, ndc_y, ndc_z, 1.0])
    world = inv @ clip
    world /= world[3]                        # perspective divide
    return tuple(world[:3])