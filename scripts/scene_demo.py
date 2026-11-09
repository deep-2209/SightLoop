import os
import numpy as np
from PIL import Image
from sightloop.sim import Simulator

def build(seed):
    sim = Simulator()
    sim.spawn_blocks(["red", "green", "yellow"], seed=seed)
    return sim

with build(0) as a, build(0) as b, build(1) as c:
    rgb_a, _ = a.capture_rgbd()
    rgb_b, _ = b.capture_rgbd()
    rgb_c, _ = c.capture_rgbd()
    print("block ids:", a.blocks)
    print("ids in mask:", np.unique(a.ground_truth_mask()))
    print("seed 0 vs seed 0 identical:", np.array_equal(rgb_a, rgb_b))
    print("seed 0 vs seed 1 identical:", np.array_equal(rgb_a, rgb_c))

    os.makedirs("outputs", exist_ok=True)
    Image.fromarray(rgb_a).save("outputs/scene_seed0.png")
    Image.fromarray(rgb_c).save("outputs/scene_seed1.png")