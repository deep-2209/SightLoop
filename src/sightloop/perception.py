"""Color-based perception. Uses ONLY the camera image — never ground truth."""
import numpy as np

from sightloop.camera import pixel_to_world
from sightloop.sim import COLORS, IMG_H, IMG_W
from sightloop.state import ObjectState

COLOR_THRESH = 0.30  # max RGB distance (0..~1.73) to call a pixel that color
MIN_PIXELS = 20      # ignore specks / stray pixels


def perceive(sim) -> list[ObjectState]:
    """Detect blocks from the RGB image. Returns the same schema as
    ground_truth_state, so perception can be scored against truth."""
    rgb, depth = sim.capture_rgbd()
    view, proj = sim.camera_matrices()
    rgbf = rgb.astype(np.float32) / 255.0

    detected = []
    for color, rgba in COLORS.items():
        target = np.array(rgba[:3], dtype=np.float32)
        dist = np.linalg.norm(rgbf - target, axis=2)
        ys, xs = np.where(dist < COLOR_THRESH)
        if len(xs) < MIN_PIXELS:
            continue  # this color isn't present (or is too occluded to see)
        u, v = int(xs.mean()), int(ys.mean())
        pos = pixel_to_world(view, proj, depth, u, v, IMG_W, IMG_H)
        detected.append(ObjectState(color, tuple(round(c, 4) for c in pos)))
    return detected