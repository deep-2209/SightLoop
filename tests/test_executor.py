import pybullet as p

from sightloop.sim import Simulator
from sightloop.state import ground_truth_state
from sightloop.executor import execute

STACK_PLAN = [
    {"tool": "pick", "args": {"color": "red"}},
    {"tool": "place_on", "args": {"color": "green"}},
]


def test_oracle_stack_succeeds_and_block_is_on_top():
    for seed in range(3):
        with Simulator() as sim:
            sim.spawn_blocks(["red", "green", "yellow"], seed=seed)
            log = execute(sim, STACK_PLAN, perceive_fn=ground_truth_state)
            assert log.success, [s.reason for s in log.steps]
            gt = {s.color: s.position for s in ground_truth_state(sim)}
            rx, ry, rz = gt["red"]
            gx, gy, _ = gt["green"]
            assert rz > 0.05  # red was lifted onto green
            assert ((rx - gx) ** 2 + (ry - gy) ** 2) ** 0.5 < 0.03


def test_missing_color_fails_cleanly():
    plan = [{"tool": "pick", "args": {"color": "orange"}}]  # not spawned
    with Simulator() as sim:
        sim.spawn_blocks(["red", "green", "yellow"], seed=0)
        log = execute(sim, plan, perceive_fn=ground_truth_state)
        assert not log.success
        assert log.steps[-1].reason == "target_not_perceived"

def test_recovery_retries_a_transient_failure(monkeypatch):
    from sightloop import control
    from sightloop.control import PickResult

    real_pick = control.pick
    state = {"n": 0}

    def flaky_pick(sim, pos):
        state["n"] += 1
        if state["n"] == 1:               # first attempt "slips"
            return PickResult(False, "slipped", 0.0, 0.0)
        return real_pick(sim, pos)        # later attempts really pick

    monkeypatch.setattr(control, "pick", flaky_pick)
    plan = [{"tool": "pick", "args": {"color": "red"}}]

    with Simulator() as sim:
        sim.spawn_blocks(["red", "green", "yellow"], seed=0)
        log = execute(sim, plan, perceive_fn=ground_truth_state, max_attempts=1)
        assert not log.success          # no-recovery: the slip ends it

    state["n"] = 0
    with Simulator() as sim:
        sim.spawn_blocks(["red", "green", "yellow"], seed=0)
        log = execute(sim, plan, perceive_fn=ground_truth_state, max_attempts=2)
        assert log.success              # recovery: retries and succeeds
        assert log.steps[0].attempts == 2