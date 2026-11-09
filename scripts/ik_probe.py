import numpy as np
import pybullet as p
from sightloop.kinematics import ARM_JOINTS, ee_position, solve_ik, within_limits
from sightloop.sim import Simulator

with Simulator() as sim:
    sim.spawn_blocks(["red", "green", "yellow"], seed=0)
    block_pos, _ = p.getBasePositionAndOrientation(
        sim.blocks["red"], physicsClientId=sim.client
    )
    target = [block_pos[0], block_pos[1], block_pos[2] + 0.15]  # hover 15 cm above
    print("target:", np.round(target, 3))

    q = solve_ik(sim, target)
    print("joint solution:", np.round(q, 3))
    print("within limits:", within_limits(sim, q))

    # Teleport joints to the solution (no physics) and ask where the tip is.
    for joint, angle in zip(ARM_JOINTS, q):
        p.resetJointState(sim.robot_id, joint, angle, physicsClientId=sim.client)
    achieved = ee_position(sim)
    error = np.linalg.norm(np.array(achieved) - np.array(target))
    print("achieved:", np.round(achieved, 3), "| error (m):", round(float(error), 5))