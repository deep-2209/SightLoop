import numpy as np
import pybullet as p
from sightloop.control import pick, place
from sightloop.sim import Simulator

TARGET = [0.45, 0.35, 0.025]  # outside the spawn region; may be hard to reach

with Simulator() as sim:
    sim.spawn_blocks(["red", "green", "yellow"], seed=0)
    for name, bid in sim.blocks.items():
        pos, _ = p.getBasePositionAndOrientation(bid, physicsClientId=sim.client)
        print(name, np.round(pos, 3))

    body = sim.blocks["red"]
    pos, _ = p.getBasePositionAndOrientation(body, physicsClientId=sim.client)
    print(pick(sim, pos))
    print(place(sim, TARGET))
    final, _ = p.getBasePositionAndOrientation(body, physicsClientId=sim.client)
    print("final:", np.round(final, 4), "| xy error:",
          round(float(np.linalg.norm(np.array(final[:2]) - np.array(TARGET[:2]))), 4))