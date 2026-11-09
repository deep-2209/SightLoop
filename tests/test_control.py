import pybullet as p

from sightloop.control import move_to
from sightloop.sim import Simulator


def test_unreachable_target_settles_short():
    with Simulator() as sim:
        result = move_to(sim, [2.0, 0.0, 0.2])
        assert not result.success
        assert result.reason == "settled_short"


def test_too_few_steps_times_out():
    with Simulator() as sim:
        sim.spawn_blocks(["red"], seed=0)
        pos, _ = p.getBasePositionAndOrientation(
            sim.blocks["red"], physicsClientId=sim.client
        )
        result = move_to(sim, [pos[0], pos[1], pos[2] + 0.15], max_steps=5)
        assert not result.success
        assert result.reason == "timeout"