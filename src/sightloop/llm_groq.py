"""Minimal Groq Chat Completions client (stdlib only), exposed as an llm_fn.
Groq is OpenAI-compatible, free tier, no credit card."""
import json
import os
import urllib.error
import urllib.request

API_URL = "https://api.groq.com/openai/v1/chat/completions"
# DEFAULT_MODEL = "llama-3.3-70b-versatile"
DEFAULT_MODEL = "openai/gpt-oss-20b"  


def make_groq_llm(model=DEFAULT_MODEL, max_tokens=512, temperature=0.0):
    """Return an llm_fn(prompt) -> text. Reads the key from the environment."""
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise RuntimeError("Set GROQ_API_KEY in your environment first.")

    def llm_fn(prompt: str) -> str:
        body = json.dumps({
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}],
        }).encode("utf-8")
        req = urllib.request.Request(
            API_URL, data=body, method="POST",
            headers={
                "Authorization": f"Bearer {key}",
                "content-type": "application/json",
                "User-Agent": "sightloop/0.1",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")
            raise RuntimeError(f"HTTP {e.code}: {detail}") from None
        if "choices" not in data:            # error payloads have no choices
            raise RuntimeError(f"API error: {data}")
        return data["choices"][0]["message"]["content"]

    return llm_fn