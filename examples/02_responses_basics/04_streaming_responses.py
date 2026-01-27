"""
Streaming responses for multi-turn conversation.
"""

# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from __future__ import annotations

import os

import fire
from llama_stack_client import LlamaStackClient
from termcolor import colored

from examples.agents.utils import check_model_is_available, get_any_available_chat_model

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - optional dependency
    load_dotenv = None


def _maybe_load_dotenv() -> None:
    if load_dotenv is not None:
        load_dotenv()


def _resolve_model(client: LlamaStackClient, model_id: str | None) -> str | None:
    resolved_model = model_id or os.getenv("LLAMA_STACK_MODEL")
    if resolved_model is None:
        return get_any_available_chat_model(client)
    if not check_model_is_available(client, resolved_model):
        return None
    return resolved_model


def _print_stream(stream) -> None:
    for event in stream:
        event_type = getattr(event, "type", None)
        if event_type == "response.output_text.delta":
            delta = getattr(event, "delta", None)
            if delta:
                print(delta, end="", flush=True)
        elif event_type == "response.completed":
            print()


def main(
    host: str,
    port: int,
    model_id: str | None = None,
    instructions: str = (
        "You are a helpful assistant. Answer directly and avoid refusing unless safety requires it."
    ),
) -> None:
    _maybe_load_dotenv()

    client = LlamaStackClient(base_url=f"http://{host}:{port}")
    resolved_model = _resolve_model(client, model_id)
    if resolved_model is None:
        print(colored("No chat-capable model available.", "red"))
        return
    print(f"Using model: {resolved_model}")

    conversation = client.conversations.create(metadata={"name": "responses-demo"})
    conversation_id = conversation.id
    print(f"Created conversation={conversation_id}")

    prompts = [
        "We are discussing Llama Stack, a framework and server for running AI models and tools. "
        "In one sentence, describe it.",
        "Summarize the description in three short bullet points.",
        "Give one concrete use case in a single sentence.",
    ]

    for prompt in prompts:
        print(colored(f"User> {prompt}", "blue"))
        response = client.responses.create(
            model=resolved_model,
            conversation=conversation_id,
            instructions=instructions,
            input=[{"role": "user", "content": prompt}],
            stream=True,
        )
        _print_stream(response)


if __name__ == "__main__":
    fire.Fire(main)
