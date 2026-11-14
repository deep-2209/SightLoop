"""Instruction + detected objects -> a validated plan, via an injected LLM."""
import json

from sightloop.tools import DIRECTIONS, validate_plan


def build_prompt(instruction, colors):
    return f"""You control a robot arm over a table with colored blocks.
Detected blocks: {sorted(colors)}
If the instruction is ambiguous or impossible with these blocks, reply with ONE
line starting "CLARIFY:" and your question. Otherwise output a JSON list of steps,
each {{"tool": NAME, "args": {{...}}}}.
Tools:
- pick(color): grasp the block of this color
- place_on(color): place the held block on top of this color's block
- place_relative(color, direction): place the held block to the
  {sorted(DIRECTIONS)} of this color's block
Instruction: "{instruction}"
Respond with ONLY the JSON list or the CLARIFY line, nothing else."""


def classify_reply(text):
    """('clarify', question) if the model declined to plan, else ('plan', None).
    A reply with no JSON list counts as a clarification."""
    s = text.strip()
    if s.upper().startswith("CLARIFY") or "[" not in s:
        q = s.split(":", 1)[1].strip() if ":" in s else s
        return ("clarify", q)
    return ("plan", None)

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