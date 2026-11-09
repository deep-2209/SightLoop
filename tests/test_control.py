import pybullet as p

from sightloop.control import move_to
from sightloop.sim import Simulator


def test_move_above_each_block_succeeds():
    for seed in range(3):
        with Simulator() as sim:
            sim.spawn_blocks(["red", "green", "yellow"], seed=seed)
            for body_id in sim.blocks.values():
                pos, _ = p.getBasePositionAndOrientation(
                    body_id, physicsClientId=sim.client
                )
                result = move_to(sim, [pos[0], pos[1], pos[2] + 0.15])
                assert result.success, result


def test_unreachable_target_fails_with_a_reason():
    with Simulator() as sim:
        result = move_to(sim, [2.0, 0.0, 0.2])
        assert not result.success
        assert result.reason in ("ik_out_of_limits", "not_reached")