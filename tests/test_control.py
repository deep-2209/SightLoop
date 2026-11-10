import pybullet as p
import numpy as np

from sightloop.control import move_to, pick, place
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

def test_pick_actually_lifts_the_block():
    for seed in range(3):
        with Simulator() as sim:
            sim.spawn_blocks(["red", "green", "yellow"], seed=seed)
            for body_id in sim.blocks.values():
                pos, _ = p.getBasePositionAndOrientation(
                    body_id, physicsClientId=sim.client
                )
                result = pick(sim, pos)
                new, _ = p.getBasePositionAndOrientation(
                    body_id, physicsClientId=sim.client
                )
                # Ground truth check: the agent-side verdict must match reality.
                assert result.success, result
                assert new[2] > 0.08, new
                break  # one block per seed; the arm now holds it

def test_pick_and_place_on_block_lands_near_target():
    for seed in range(3):
        with Simulator() as sim:
            sim.spawn_blocks(["red", "green", "yellow"], seed=seed)
            red, green = sim.blocks["red"], sim.blocks["green"]
            rpos, _ = p.getBasePositionAndOrientation(red, physicsClientId=sim.client)
            gpos, _ = p.getBasePositionAndOrientation(green, physicsClientId=sim.client)

            assert pick(sim, gpos).success
            target = [rpos[0], rpos[1], 0.075]  # green's center, on top of red
            result = place(sim, target)
            assert result.success, result

            sim.step(240)  # let the stack settle or topple
            final, _ = p.getBasePositionAndOrientation(green, physicsClientId=sim.client)
            assert np.linalg.norm(np.array(final[:2]) - np.array(target[:2])) < 0.02
            assert abs(final[2] - 0.075) < 0.02  # still on top, not fallen to ~0.025