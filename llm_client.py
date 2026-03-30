"""
LLM client supporting AMD Gateway for both OpenAI (GPT4o) and Anthropic (Claude) models.
"""

from __future__ import annotations

import os
import json
from dataclasses import dataclass
from typing import Optional, List, Dict

AMD_GATEWAY_OPENAI_URL = "https://llm-api.amd.com/OpenAI"
AMD_GATEWAY_ANTHROPIC_URL = "https://llm-api.amd.com/Anthropic"
AMD_AUTH_HEADER = "Ocp-Apim-Subscription-Key"

ANTHROPIC_MODELS = {"claude-opus-4.6", "claude-sonnet-4.5", "claude-sonnet-4", "claude-haiku-3.5"}


@dataclass
class LLMConfig:
    api_key: str = ""
    model: str = "GPT4o"
    temperature: float = 0.7
    max_tokens: int = 8000

    @classmethod
    def from_env(cls, model: Optional[str] = None) -> "LLMConfig":
        return cls(
            api_key=os.environ.get("AMD_LLM_API_KEY", os.environ.get("LLM_API_KEY", os.environ.get("LLM_GATEWAY_KEY", ""))),
            model=model or os.environ.get("LLM_MODEL_NAME", "GPT4o"),
        )

    @property
    def is_anthropic(self) -> bool:
        return any(self.model.startswith(prefix) for prefix in ("claude-",))


class LLMClient:
    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig.from_env()
        if not self.config.api_key:
            raise ValueError("No API key found. Set AMD_LLM_API_KEY or LLM_API_KEY env var.")

        if self.config.is_anthropic:
            self._init_anthropic()
        else:
            self._init_openai()

    def _init_openai(self):
        import openai
        self._provider = "openai"
        self._client = openai.OpenAI(
            base_url=AMD_GATEWAY_OPENAI_URL,
            api_key="dummy",
            default_headers={AMD_AUTH_HEADER: self.config.api_key},
        )

    def _init_anthropic(self):
        from anthropic import Anthropic
        from httpx import Timeout
        self._provider = "anthropic"
        try:
            user = os.getlogin()
        except Exception:
            user = os.getenv("USERNAME", "debug_arena")
        self._client = Anthropic(
            base_url=AMD_GATEWAY_ANTHROPIC_URL,
            api_key="dummy",
            default_headers={
                AMD_AUTH_HEADER: self.config.api_key,
                "user": user,
                "anthropic-version": "2023-10-16",
            },
            timeout=Timeout(connect=15.0, read=600.0, write=30.0, pool=30.0),
        )

    def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        response_format: Optional[dict] = None,
    ) -> str:
        temp = temperature if temperature is not None else self.config.temperature
        tokens = max_tokens or self.config.max_tokens

        if self._provider == "anthropic":
            return self._generate_anthropic(prompt, system_prompt, temp, tokens)
        return self._generate_openai(prompt, system_prompt, temp, tokens, response_format)

    def _generate_openai(self, prompt, system_prompt, temperature, max_tokens, response_format=None) -> str:
        import time as _time
        import random as _random

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        params = {
            "model": self.config.model,
            "messages": messages,
            "max_completion_tokens": max_tokens,
            "temperature": temperature,
        }
        if response_format:
            params["response_format"] = response_format

        max_retries = 5
        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                response = self._client.chat.completions.create(**params)
                return response.choices[0].message.content
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                is_transient = any(kw in error_str for kw in [
                    "connection", "timeout", "429", "rate", "500", "502", "503", "504",
                    "overloaded", "temporarily", "service", "bad gateway",
                ])
                if is_transient and attempt < max_retries:
                    base_wait = min(2 ** attempt, 30)
                    jitter = _random.uniform(0, base_wait * 0.5)
                    _time.sleep(base_wait + jitter)
                else:
                    raise

        raise last_error

    def _generate_anthropic(self, prompt, system_prompt, temperature, max_tokens) -> str:
        import time as _time
        import random as _random

        kwargs = {
            "model": self.config.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        max_retries = 6
        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                response = self._client.messages.create(**kwargs)
                return response.content[0].text
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                is_transient = any(kw in error_str for kw in [
                    "connection", "timeout", "429", "rate", "500", "502", "503", "504",
                    "overloaded", "temporarily", "service", "bad gateway",
                ])
                if is_transient and attempt < max_retries:
                    base_wait = min(2 ** attempt, 30)
                    jitter = _random.uniform(0, base_wait * 0.5)
                    _time.sleep(base_wait + jitter)
                else:
                    raise

        raise last_error

    def generate_json(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.3,
    ) -> dict:
        raw = self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
        )
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            cleaned = "\n".join(lines)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        # Opus often outputs valid JSON followed by extra commentary.
        # Find the outermost matching {} and extract just that.
        start = cleaned.find("{")
        if start == -1:
            raise json.JSONDecodeError("No JSON object found in response", cleaned, 0)

        depth = 0
        in_string = False
        escape = False
        for i in range(start, len(cleaned)):
            c = cleaned[i]
            if escape:
                escape = False
                continue
            if c == '\\' and in_string:
                escape = True
                continue
            if c == '"' and not escape:
                in_string = not in_string
                continue
            if in_string:
                continue
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    return json.loads(cleaned[start:i + 1])

        raise json.JSONDecodeError("No complete JSON object found", cleaned, 0)

    def _retry_call(self, fn, max_retries=5):
        """Generic retry wrapper for transient errors."""
        import time as _time
        import random as _random

        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                return fn()
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                is_transient = any(kw in error_str for kw in [
                    "connection", "timeout", "429", "rate", "500", "502", "503", "504",
                    "overloaded", "temporarily", "service", "bad gateway",
                ])
                if is_transient and attempt < max_retries:
                    base_wait = min(2 ** attempt, 30)
                    jitter = _random.uniform(0, base_wait * 0.5)
                    _time.sleep(base_wait + jitter)
                else:
                    raise
        raise last_error

    def chat(
        self,
        messages: list[dict],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        temp = temperature if temperature is not None else self.config.temperature
        tokens = max_tokens or self.config.max_tokens

        if self._provider == "anthropic":
            system_prompt = ""
            chat_msgs = []
            for m in messages:
                if m["role"] == "system":
                    system_prompt = m["content"]
                else:
                    chat_msgs.append(m)
            kwargs = {
                "model": self.config.model,
                "max_tokens": tokens,
                "temperature": temp,
                "messages": chat_msgs,
            }
            if system_prompt:
                kwargs["system"] = system_prompt
            return self._retry_call(
                lambda: self._client.messages.create(**kwargs).content[0].text
            )

        params = {
            "model": self.config.model,
            "messages": messages,
            "max_completion_tokens": tokens,
            "temperature": temp,
        }
        return self._retry_call(
            lambda: self._client.chat.completions.create(**params).choices[0].message.content
        )
