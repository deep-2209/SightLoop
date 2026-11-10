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
    attempts: int = 1


@dataclass
class EpisodeLog:
    steps: list = field(default_factory=list)

    @property
    def success(self) -> bool:
        return bool(self.steps) and all(s.ok for s in self.steps)


def execute(sim, plan, perceive_fn=perceive, max_attempts=1) -> EpisodeLog:
    """Run each step, retrying up to max_attempts with fresh perception each
    time. max_attempts=1 is the no-recovery baseline; >1 enables recovery.
    Stops the episode on a step that fails all its attempts."""
    log = EpisodeLog()
    for call in plan:
        tool, args = call["tool"], call["args"]
        ok, reason, attempts = False, "", 0

        while attempts < max_attempts and not ok:
            attempts += 1
            seen = {o.color: o.position for o in perceive_fn(sim)}  # fresh look
            color = args["color"]
            if color not in seen:
                ok, reason = False, "target_not_perceived"
                continue
            tx, ty, _ = seen[color]
            if tool == "pick":
                r = control.pick(sim, [tx, ty, TABLE_Z])
            elif tool == "place_on":
                r = control.place(sim, [tx, ty, STACK_Z])
            elif tool == "place_relative":
                dx, dy = DIR_OFFSET[args["direction"]]
                r = control.place(sim, [tx + dx, ty + dy, TABLE_Z])
            else:
                ok, reason = False, "unknown_tool"
                break
            ok, reason = r.success, r.reason

        log.steps.append(StepLog(tool, args, ok, reason, attempts))
        if not ok:
            break  # episode halts when a step exhausts its attempts
    return log