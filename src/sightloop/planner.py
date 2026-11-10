"""Instruction + detected objects -> a validated plan, via an injected LLM."""
import json

from sightloop.tools import DIRECTIONS, validate_plan


def build_prompt(instruction, colors):
    return f"""You control a robot arm over a table with colored blocks.
Detected blocks: {sorted(colors)}
Output a JSON list of steps. Each step is {{"tool": NAME, "args": {{...}}}}.
Tools:
- pick(color): grasp the block of this color
- place_on(color): place the held block on top of this color's block
- place_relative(color, direction): place the held block to the
  {sorted(DIRECTIONS)} of this color's block
Instruction: "{instruction}"
Respond with ONLY the JSON list, no prose."""


def parse_plan(text):
    """Pull the JSON list out of the model reply. None if it can't be parsed."""
    text = text.strip()
    start, end = text.find("["), text.rfind("]")
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return None


def plan(instruction, colors, llm_fn):
    """llm_fn: prompt -> raw model text. Injected so we can test offline and
    swap providers. Returns (parsed_plan_or_None, ValidationResult)."""
    raw = llm_fn(build_prompt(instruction, colors))
    parsed = parse_plan(raw)
    if parsed is None:
        return None, validate_plan([], colors)  # unparseable counts as invalid
    return parsed, validate_plan(parsed, colors)