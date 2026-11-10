from sightloop.sim import Simulator
from sightloop.perception import perceive
from sightloop.planner import plan
from sightloop.executor import execute
from sightloop.llm_anthropic import make_anthropic_llm
from sightloop.llm_openai import make_openai_llm
from sightloop.llm_groq import make_groq_llm

INSTRUCTION = "stack the red block on the green block"
# llm_fn = make_anthropic_llm() # uncomment to test Anthropic instead of OpenAI or Groq
# llm_fn = make_openai_llm()  # uncomment to test OpenAI instead of Anthropic or Groq
llm_fn = make_groq_llm() # uncomment to test Groq instead of OpenAI or Anthropic

with Simulator() as sim:
    sim.spawn_blocks(["red", "green", "yellow"], seed=0)
    colors = {o.color for o in perceive(sim)}
    print("perceived:", sorted(colors))

    parsed, validation = plan(INSTRUCTION, colors, llm_fn)
    print("plan:", parsed)
    print("valid:", validation.valid, "errors:", validation.errors)

    if validation.valid:
        log = execute(sim, parsed, max_attempts=2)
        for s in log.steps:
            print(f"  {s.tool}{tuple(s.args.values())}: ok={s.ok} ({s.reason})")
        print("episode success:", log.success)