from sightloop.sim import Simulator
from sightloop.perception import perceive
from sightloop.planner import build_prompt, classify_reply
from sightloop.llm_groq import make_groq_llm
from sightloop.tasks import generate_tasks
from sightloop.metrics import ambiguity_scores

llm = make_groq_llm()
tasks = generate_tasks(n=20, master_seed=0)
ambiguous = [t for t in tasks if t.ambiguous]
clear = [t for t in tasks if not t.ambiguous][:8]   # clear controls

records = []
for t in ambiguous + clear:
    with Simulator() as sim:
        sim.spawn_blocks(list(t.colors), seed=t.seed)
        colors = {o.color for o in perceive(sim)}
    kind, question = classify_reply(llm(build_prompt(t.instruction, colors)))
    records.append({"ambiguous": t.ambiguous, "clarified": kind == "clarify"})
    if t.ambiguous:
        print(f"[{t.task_id}] {t.instruction!r}")
        print(f"   clarified={kind == 'clarify'}  produced={question!r}")
        print(f"   reference={t.reference_clarification!r}\n")

det, fa = ambiguity_scores(records)
print(f"ambiguity detection rate:          {det:.0%}")
print(f"over-clarification on clear tasks: {fa:.0%}")