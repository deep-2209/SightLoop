import numpy as np
from sightloop.sim import Simulator, IMG_W, IMG_H
from sightloop.state import ground_truth_state
from sightloop.camera import pixel_to_world


def test_unproject_matches_ground_truth_xy():
    with Simulator() as sim:
        sim.spawn_blocks(["red", "green", "yellow"], seed=0)
        _, depth = sim.capture_rgbd()
        mask = sim.ground_truth_mask()
        view, proj = sim.camera_matrices()
        truth = {s.color: s.position for s in ground_truth_state(sim)}
        for color, body_id in sim.blocks.items():
            ys, xs = np.where(mask == body_id)
            u, v = int(xs.mean()), int(ys.mean())
            wx, wy, _ = pixel_to_world(view, proj, depth, u, v, IMG_W, IMG_H)
            tx, ty, _ = truth[color]
            assert ((wx - tx) ** 2 + (wy - ty) ** 2) ** 0.5 < 0.015