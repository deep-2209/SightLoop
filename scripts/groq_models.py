import json
import os
import urllib.request

req = urllib.request.Request(
    "https://api.groq.com/openai/v1/models",
    headers={
        "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
        "User-Agent": "sightloop/0.1",
    },
)
with urllib.request.urlopen(req, timeout=30) as r:
    data = json.loads(r.read())

for m in data.get("data", []):
    print(m["id"])