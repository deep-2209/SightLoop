"""Execute a validated symbolic plan against the simulator."""
from dataclasses import dataclass, field

from sightloop import control
from sightloop.perception import perceive

TABLE_Z = 0.025        # center height of a block on the table
STACK_Z = 0.075        # center height of a block resting on another block
PLACE_OFFSET = 0.08    # lateral spacing for place_relative (meters). Distance between blocks for relative placement.

# robot faces +x; "left" is +y. Documented so direction semantics are fixed.
DIR_OFFSET = {
    "left":  (0.0,  PLACE_OFFSET),
    "right": (0.0, -PLACE_OFFSET),
    "back":  (PLACE_OFFSET, 0.0),
    "front": (-PLACE_OFFSET, 0.0),
}


@dataclass
class StepLog:
    tool: str
    args: dict
    ok: bool
    reason: str


@dataclass
class EpisodeLog:
    steps: list = field(default_factory=list)

    @property
    def success(self) -> bool:
        return bool(self.steps) and all(s.ok for s in self.steps)


def execute(sim, plan, perceive_fn=perceive) -> EpisodeLog:
    """Run each step. Resolve colors via perceive_fn (pass ground_truth_state
    for the oracle). Stop on the first failed step (no-recovery behavior)."""
    log = EpisodeLog()
    for call in plan:
        tool, args = call["tool"], call["args"]
        seen = {o.color: o.position for o in perceive_fn(sim)}
        color = args["color"]
        if color not in seen:
            log.steps.append(StepLog(tool, args, False, "target_not_perceived"))
            break

        tx, ty, _ = seen[color]
        if tool == "pick":
            r = control.pick(sim, [tx, ty, TABLE_Z])
        elif tool == "place_on":
            r = control.place(sim, [tx, ty, STACK_Z])
        elif tool == "place_relative":
            dx, dy = DIR_OFFSET[args["direction"]]
            r = control.place(sim, [tx + dx, ty + dy, TABLE_Z])
        else:
            log.steps.append(StepLog(tool, args, False, "unknown_tool"))
            break

        log.steps.append(StepLog(tool, args, r.success, r.reason))
        if not r.success:
            break  # no-recovery: halt on first failure
    return log