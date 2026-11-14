from sightloop.metrics import load_rows, plan_validity_rate, success_by_condition

for model in ["openai/gpt-oss-20b", "qwen/qwen3.8-27b", "openai/gpt-oss-120b"]:
    slug = model.replace("/", "_")
    rows = load_rows(f"results_{slug}.jsonl")
    sc = success_by_condition(rows)
    print(f"{model:24} valid={plan_validity_rate(rows):.0%} "
          f"base={sc['baseline']:.0%} oracle={sc['oracle']:.0%} "
          f"recover={sc['fault_recover']:.0%}")