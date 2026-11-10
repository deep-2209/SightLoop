"""Minimal Anthropic Messages API client (stdlib only), exposed as an llm_fn."""
import json
import os
import urllib.request

API_URL = "https://api.anthropic.com/v1/messages"
DEFAULT_MODEL = "claude-haiku-5-5"  


def make_anthropic_llm(model=DEFAULT_MODEL, max_tokens=512, temperature=0.0):
    """Return an llm_fn(prompt) -> text. Reads the key from the environment."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("Set ANTHROPIC_API_KEY in your environment first.")

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
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        if "content" not in data:               # error payloads have no content
            raise RuntimeError(f"API error: {data}")
        return data["content"][0]["text"]

    return llm_fn