import pybullet as p

from sightloop.sim import Simulator
from sightloop.state import ground_truth_state
from sightloop.executor import execute
from sightloop.faults import Fault

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