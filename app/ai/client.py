from __future__ import annotations

import os
from typing import Protocol

from openai import OpenAI


class ChatClient(Protocol):
    def complete(self, system_prompt: str, user_prompt: str, model: str, temperature: float, max_tokens: int) -> str: ...


class OpenAIChatClient:
    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set")
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def complete(self, system_prompt: str, user_prompt: str, model: str, temperature: float = 0.2, max_tokens: int = 1000) -> str:
        resp = self.client.chat.completions.create(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return resp.choices[0].message.content or ""


class MockChatClient:
    def __init__(self, response: str):
        self.response = response

    def complete(self, system_prompt: str, user_prompt: str, model: str, temperature: float, max_tokens: int) -> str:
        return self.response


