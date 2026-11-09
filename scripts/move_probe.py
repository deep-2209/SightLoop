import pybullet as p
from sightloop.control import move_to
from sightloop.sim import Simulator

with Simulator() as sim:
    sim.spawn_blocks(["red", "green", "yellow"], seed=0)
    for name, body_id in sim.blocks.items():
        pos, _ = p.getBasePositionAndOrientation(body_id, physicsClientId=sim.client)
        target = [pos[0], pos[1], pos[2] + 0.15]
        print(name, move_to(sim, target))

    print("unreachable:", move_to(sim, [2.0, 0.0, 0.2]))