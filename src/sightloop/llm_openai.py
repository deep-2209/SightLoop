"""Minimal OpenAI Chat Completions client (stdlib only), exposed as an llm_fn."""
import json
import os
import urllib.request
import urllib.error

API_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-4o-mini"  


def make_openai_llm(model=DEFAULT_MODEL, max_tokens=512, temperature=0.0):
    """Return an llm_fn(prompt) -> text. Reads the key from the environment."""
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("Set OPENAI_API_KEY in your environment first.")

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
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")
            raise RuntimeError(f"HTTP {e.code}: {detail}") from None
        return data["choices"][0]["message"]["content"]

    return llm_fn