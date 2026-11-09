"""Low-level motion primitives. Every primitive returns a typed result."""
from dataclasses import dataclass

import numpy as np
import pybullet as p

from sightloop.kinematics import ARM_JOINTS, ee_position, solve_ik, within_limits


@dataclass(frozen=True)
class MoveResult:
    success: bool
    reason: str            # "ok" | "ik_out_of_limits" | "not_reached"
    position_error: float  # meters, gripper tip vs target (nan if we never moved)
    steps_used: int


def move_to(
    sim,
    target_pos,
    max_steps: int = 720,   # 3 simulated seconds at 240 Hz
    joint_tol: float = 1e-3,  # radians: "settled" threshold per joint
    pos_tol: float = 0.01,    # meters: how close counts as "arrived"
) -> MoveResult:
    q_target = solve_ik(sim, target_pos)
    if not within_limits(sim, q_target):
        return MoveResult(False, "ik_out_of_limits", float("nan"), 0)

    forces = [
        p.getJointInfo(sim.robot_id, j, physicsClientId=sim.client)[10]
        for j in ARM_JOINTS
    ]
    p.setJointMotorControlArray(
        sim.robot_id,
        ARM_JOINTS,
        p.POSITION_CONTROL,
        targetPositions=q_target,
        forces=forces,
        physicsClientId=sim.client,
    )

    steps = 0
    while steps < max_steps:
        sim.step()
        steps += 1
        q_now = [
            p.getJointState(sim.robot_id, j, physicsClientId=sim.client)[0]
            for j in ARM_JOINTS
        ]
        if max(abs(a - b) for a, b in zip(q_now, q_target)) < joint_tol:
            break

    error = float(np.linalg.norm(np.array(ee_position(sim)) - np.array(target_pos)))
    ok = error <= pos_tol
    return MoveResult(ok, "ok" if ok else "not_reached", error, steps)