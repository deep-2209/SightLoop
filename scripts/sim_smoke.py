import pybullet as p
from sightloop.sim import Simulator

with Simulator() as sim:
    print("client:", sim.client, "| plane:", sim.plane_id, "| robot:", sim.robot_id)
    sim.step(240)
    pos, _ = p.getBasePositionAndOrientation(sim.robot_id, physicsClientId=sim.client)
    print("base after 240 steps:", pos)