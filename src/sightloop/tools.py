"""Agent-facing tool schema (symbolic) and plan validation."""
from dataclasses import dataclass

DIRECTIONS = {"left", "right", "front", "back"}

# tool name -> the exact set of argument names it requires
TOOL_SCHEMA = {
    "pick": {"color"},
    "place_on": {"color"},
    "place_relative": {"color", "direction"},
}


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: list[str]


def validate_plan(plan, known_colors) -> ValidationResult:
    """A plan is valid if every step names a real tool, has exactly the right
    args, and references only detected colors. Does NOT judge correctness."""
    errors = []
    if not isinstance(plan, list) or not plan:
        return ValidationResult(False, ["plan is not a non-empty list"])
    for i, call in enumerate(plan):
        if not isinstance(call, dict) or "tool" not in call:
            errors.append(f"step {i}: not a tool-call object")
            continue
        tool, args = call.get("tool"), call.get("args", {})
        if tool not in TOOL_SCHEMA:
            errors.append(f"step {i}: unknown tool '{tool}'")
            continue
        if not isinstance(args, dict) or set(args) != TOOL_SCHEMA[tool]:
            errors.append(f"step {i}: {tool} has wrong args {set(args)}")
            continue
        if args["color"] not in known_colors:
            errors.append(f"step {i}: color '{args['color']}' not detected")
        if tool == "place_relative" and args["direction"] not in DIRECTIONS:
            errors.append(f"step {i}: bad direction '{args['direction']}'")
    return ValidationResult(len(errors) == 0, errors)