from sightloop.batch import Condition, make_cached_llm, run_batch
from sightloop.faults import Fault
from sightloop.llm_groq import make_groq_llm
from sightloop.tasks import generate_tasks, split_tasks

MODELS = ["openai/gpt-oss-20b", "qwen/qwen3.8-27b", "openai/gpt-oss-120b"]
CONDITIONS = [
    Condition("baseline"),
    Condition("oracle", use_oracle=True),
    Condition("fault_norecover", max_attempts=1, fault=Fault("mis_grasp", 0)),
    Condition("fault_recover",   max_attempts=2, fault=Fault("mis_grasp", 0)),
]
val, _ = split_tasks(generate_tasks(n=40, master_seed=0))

for model in MODELS:
    slug = model.replace("/", "_")
    llm = make_cached_llm(make_groq_llm(model=model), f"cache_{slug}.json", throttle=2.5)
    rows = run_batch(val, CONDITIONS, llm, f"results_{slug}.jsonl")
    print(f"{model}: {len(rows)} rows -> results_{slug}.jsonl")