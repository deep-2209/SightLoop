"""Inverse/forward kinematics helpers for the Panda arm."""
import pybullet as p

ARM_JOINTS = [0, 1, 2, 3, 4, 5, 6]
FINGER_JOINTS = [9, 10]
# IK expects limit/rest lists for exactly these joints, in this order (9 values).
MOVABLE_JOINTS = ARM_JOINTS + FINGER_JOINTS
EE_LINK = 11  # panda_grasptarget (see joint table)
# Quaternion (x, y, z, w): 180-degree rotation about x, so the gripper points down.
DOWN_ORN = (1.0, 0.0, 0.0, 0.0)

# A bent-elbow "ready" pose. Every value was checked against the limits in the
# joint table (e.g. joint 4 is -2.356, inside [-3.14, 0]).
HOME_POSE = [0.0, -0.785, 0.0, -2.356, 0.0, 1.571, 0.785]
FINGER_OPEN = 0.04  # upper limit of the finger joints = fully open


def set_home_pose(sim) -> None:
    """Teleport the arm to HOME_POSE, open the gripper, and hold it there."""
    c = sim.client
    targets = dict(zip(ARM_JOINTS, HOME_POSE))
    targets.update({j: FINGER_OPEN for j in FINGER_JOINTS})
    for joint, angle in targets.items():
        p.resetJointState(sim.robot_id, joint, angle, physicsClientId=c)
        max_force = p.getJointInfo(sim.robot_id, joint, physicsClientId=c)[10]
        p.setJointMotorControl2(
            sim.robot_id,
            joint,
            p.POSITION_CONTROL,
            targetPosition=angle,
            force=max_force,
            physicsClientId=c,
        )


def _ik_arrays(sim):
    """Limits, ranges and rest pose for the 9 movable joints."""
    lows, highs = [], []
    for j in MOVABLE_JOINTS:
        info = p.getJointInfo(sim.robot_id, j, physicsClientId=sim.client)
        lows.append(info[8])
        highs.append(info[9])
    ranges = [hi - lo for lo, hi in zip(lows, highs)]
    rest = HOME_POSE + [FINGER_OPEN] * len(FINGER_JOINTS)
    return lows, highs, ranges, rest


def solve_ik(sim, target_pos, target_orn=DOWN_ORN) -> list[float]:
    """Joint angles for the 7 arm joints that should put the gripper tip at
    target_pos, staying inside joint limits and near HOME_POSE.
    Still a numerical solution: always verify it."""
    lows, highs, ranges, rest = _ik_arrays(sim)
    solution = p.calculateInverseKinematics(
        sim.robot_id,
        EE_LINK,
        list(target_pos),
        list(target_orn),
        lowerLimits=lows,
        upperLimits=highs,
        jointRanges=ranges,
        restPoses=rest,
        maxNumIterations=200,
        residualThreshold=1e-4,
        physicsClientId=sim.client,
    )
    return list(solution[: len(ARM_JOINTS)])


def joint_limits(sim) -> tuple[list[float], list[float]]:
    lows, highs = [], []
    for j in ARM_JOINTS:
        info = p.getJointInfo(sim.robot_id, j, physicsClientId=sim.client)
        lows.append(info[8])
        highs.append(info[9])
    return lows, highs


def within_limits(sim, q: list[float]) -> bool:
    lows, highs = joint_limits(sim)
    return all(lo <= v <= hi for v, lo, hi in zip(q, lows, highs))


def ee_position(sim) -> tuple[float, float, float]:
    """Where the gripper tip is NOW (forward kinematics)."""
    state = p.getLinkState(
        sim.robot_id,
        EE_LINK,
        computeForwardKinematics=True,
        physicsClientId=sim.client,
    )
    return state[4]