import pybullet as p
from sightloop.control import pick
from sightloop.sim import Simulator

with Simulator() as sim:
    sim.spawn_blocks(["red", "green", "yellow"], seed=0)
    body = sim.blocks["red"]
    info = p.getDynamicsInfo(body, -1, physicsClientId=sim.client)
    print("block mass, lateral friction:", info[0], info[1])

    pos, _ = p.getBasePositionAndOrientation(body, physicsClientId=sim.client)
    print("start block z:", round(pos[2], 4))
    print(pick(sim, pos))
    pos2, _ = p.getBasePositionAndOrientation(body, physicsClientId=sim.client)
    print("end block z:  ", round(pos2[2], 4))  