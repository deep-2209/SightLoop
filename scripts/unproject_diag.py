import numpy as np
from sightloop.sim import Simulator, IMG_W, IMG_H
from sightloop.state import ground_truth_state
from sightloop.camera import pixel_to_world

with Simulator() as sim:
    sim.spawn_blocks(["red", "green", "yellow"], seed=0)
    _, depth = sim.capture_rgbd()
    mask = sim.ground_truth_mask()     # eval-only: used ONLY to locate blocks here
    view, proj = sim.camera_matrices()
    truth = {s.color: s.position for s in ground_truth_state(sim)}

    for color, body_id in sim.blocks.items():
        ys, xs = np.where(mask == body_id)
        if len(xs) == 0:
            print(color, "not visible"); continue
        u, v = int(xs.mean()), int(ys.mean())          # centroid pixel
        wx, wy, wz = pixel_to_world(view, proj, depth, u, v, IMG_W, IMG_H)
        tx, ty, _ = truth[color]
        err = ((wx - tx) ** 2 + (wy - ty) ** 2) ** 0.5
        print(f"{color:7} world=({wx:.3f},{wy:.3f},{wz:.3f}) "
              f"truth=({tx:.3f},{ty:.3f}) xy_err={err:.4f}")