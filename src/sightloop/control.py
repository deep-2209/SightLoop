"""Low-level motion primitives. Every primitive returns a typed result."""
from dataclasses import dataclass

import numpy as np
import pybullet as p

from sightloop.kinematics import ARM_JOINTS, ee_position, solve_ik, within_limits, FINGER_JOINTS, FINGER_OPEN


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
    settled = False
    while steps < max_steps:
        sim.step()
        steps += 1
        q_now = [
            p.getJointState(sim.robot_id, j, physicsClientId=sim.client)[0]
            for j in ARM_JOINTS
        ]
        if max(abs(a - b) for a, b in zip(q_now, q_target)) < joint_tol:
            settled = True
            break

    error = float(np.linalg.norm(np.array(ee_position(sim)) - np.array(target_pos)))
    if error <= pos_tol:
        reason = "ok"
    elif settled:
        reason = "settled_short"
    else:
        reason = "timeout"
    return MoveResult(reason == "ok", reason, error, steps)


@dataclass(frozen=True)
class GripperResult:
    width: float   # meters: sum of both finger positions (0 closed, 0.08 open)
    settled: bool  # False if still moving when time ran out
    steps_used: int


def gripper_width(sim) -> float:
    return sum(
        p.getJointState(sim.robot_id, j, physicsClientId=sim.client)[0]
        for j in FINGER_JOINTS
    )


def set_gripper(
    sim,
    opening: float,           # per-finger target, 0.0 (closed) .. 0.04 (open)
    max_steps: int = 120,
    min_steps: int = 10,      # don't judge "settled" before the fingers start moving
    vel_tol: float = 1e-3,    # m/s: below this a finger counts as stopped
) -> GripperResult:
    opening = min(max(opening, 0.0), FINGER_OPEN)  # clamp to the joint range
    forces = [
        p.getJointInfo(sim.robot_id, j, physicsClientId=sim.client)[10]
        for j in FINGER_JOINTS
    ]
    p.setJointMotorControlArray(
        sim.robot_id,
        FINGER_JOINTS,
        p.POSITION_CONTROL,
        targetPositions=[opening] * len(FINGER_JOINTS),
        forces=forces,
        physicsClientId=sim.client,
    )

    steps, settled = 0, False
    while steps < max_steps:
        sim.step()
        steps += 1
        if steps >= min_steps:
            vels = [
                p.getJointState(sim.robot_id, j, physicsClientId=sim.client)[1]
                for j in FINGER_JOINTS
            ]
            if max(abs(v) for v in vels) < vel_tol:
                settled = True
                break
    return GripperResult(gripper_width(sim), settled, steps)