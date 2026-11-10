import pybullet as p

from sightloop.sim import Simulator
from sightloop.state import ground_truth_state
from sightloop.executor import execute
from sightloop.faults import Fault
from sightloop.perception import perceive
from sightloop.faults import inject_scene_fault

PICK_PLAN = [{"tool": "pick", "args": {"color": "red"}}]


def test_misgrasp_sinks_no_recovery_but_recovery_saves_it():
    fault = Fault(kind="mis_grasp", step=0)

    # no-recovery: the injected mis-grasp ends the episode
    with Simulator() as sim:
        sim.spawn_blocks(["red", "green", "yellow"], seed=0)
        log = execute(sim, PICK_PLAN, perceive_fn=ground_truth_state,
                      max_attempts=1, fault=fault)
        assert not log.success
        assert log.steps[0].reason == "gripper_empty"

    # recovery: it retries clean and succeeds on attempt 2
    with Simulator() as sim:
        sim.spawn_blocks(["red", "green", "yellow"], seed=0)
        log = execute(sim, PICK_PLAN, perceive_fn=ground_truth_state,
                      max_attempts=2, fault=fault)
        assert log.success
        assert log.steps[0].attempts == 2

def test_dropped_is_recoverable():
    fault = Fault(kind="dropped", step=0)
    with Simulator() as sim:
        sim.spawn_blocks(["red", "green", "yellow"], seed=0)
        log = execute(sim, PICK_PLAN, perceive_fn=ground_truth_state,
                      max_attempts=1, fault=fault)
        assert not log.success
        assert log.steps[0].reason == "dropped"
    with Simulator() as sim:
        sim.spawn_blocks(["red", "green", "yellow"], seed=0)
        log = execute(sim, PICK_PLAN, perceive_fn=ground_truth_state,
                      max_attempts=2, fault=fault)
        assert log.success


def test_occlusion_defeats_recovery_but_not_the_oracle():
    fault = Fault(kind="occlusion", step=0, target="red")

    # real perception: blinded, and retrying doesn't help
    for attempts in (1, 2):
        with Simulator() as sim:
            sim.spawn_blocks(["red", "green", "yellow"], seed=0)
            inject_scene_fault(sim, fault)
            log = execute(sim, PICK_PLAN, perceive_fn=perceive,
                          max_attempts=attempts, fault=fault)
            assert not log.success
            assert log.steps[0].reason == "target_not_perceived"

    # oracle: reads ground truth, sees through the occluder, succeeds
    with Simulator() as sim:
        sim.spawn_blocks(["red", "green", "yellow"], seed=0)
        inject_scene_fault(sim, fault)
        log = execute(sim, PICK_PLAN, perceive_fn=ground_truth_state, max_attempts=1)
        assert log.success