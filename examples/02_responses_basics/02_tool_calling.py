"""
Tool calling with the Responses API.
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

from examples.agents.utils import check_model_is_available

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover - optional dependency
    load_dotenv = None


def _maybe_load_dotenv() -> None:
    if load_dotenv is not None:
        load_dotenv()


def _get_model_type(model) -> str | None:
    for attr in ("model_type", "type", "model_kind", "kind", "model_family"):
        value = getattr(model, attr, None)
        if isinstance(value, str):
            return value
    for metadata_attr in ("custom_metadata", "metadata"):
        metadata = getattr(model, metadata_attr, None)
        if isinstance(metadata, dict):
            value = metadata.get("model_type") or metadata.get("type")
            if isinstance(value, str):
                return value
    return None


def _get_model_id(model) -> str | None:
    for attr in ("identifier", "model_id", "id", "name"):
        value = getattr(model, attr, None)
        if isinstance(value, str):
            return value
    return None


def _get_any_llm_model(client: LlamaStackClient) -> str | None:
    for model in client.models.list():
        model_id = _get_model_id(model)
        if not model_id or "guard" in model_id:
            continue
        lowered = model_id.lower()
        if "embed" in lowered or "embedding" in lowered or "minilm" in lowered:
            continue
        model_type = _get_model_type(model)
        if model_type is None or model_type == "llm":
            return model_id
    return None


def _resolve_model(client: LlamaStackClient, model_id: str | None) -> str | None:
    resolved_model = model_id or os.getenv("LLAMA_STACK_MODEL")
    if resolved_model is None:
        return _get_any_llm_model(client)
    if not check_model_is_available(client, resolved_model):
        return None
    return resolved_model


def _print_response(response) -> None:
    if response.output_text:
        print(f"[responses] answer: {response.output_text}")
    else:
        print("[responses] answer: (empty)")

    print("[responses] output items:")
    for item in response.output:
        item_type = getattr(item, "type", None)
        status = getattr(item, "status", None)
        print(f"- type={item_type} status={status}")
        if item_type == "web_search_call":
            print(f"  id={getattr(item, 'id', None)}")


def main(
    host: str,
    port: int,
    model_id: str | None = None,
    prompt: str = "What is Llama Stack?",
) -> None:
    _maybe_load_dotenv()

    client = LlamaStackClient(base_url=f"http://{host}:{port}")
    resolved_model = _resolve_model(client, model_id)
    print(f"Using model: {resolved_model}")
    if resolved_model is None:
        return

    if "TAVILY_SEARCH_API_KEY" not in os.environ and "BRAVE_SEARCH_API_KEY" not in os.environ:
        print(
            colored(
                "Warning: TAVILY_SEARCH_API_KEY or BRAVE_SEARCH_API_KEY is not set; web search may not work.",
                "yellow",
            )
        )

    response = client.responses.create(
        model=resolved_model,
        instructions=(
            "Use web search to answer the question and provide a short, factual reply."
        ),
        input=[{"role": "user", "content": prompt}],
        tools=[{"type": "web_search"}],
        tool_choice={"type": "web_search"},
        include=["web_search_call.action.sources"],
        stream=False,
    )
    _print_response(response)


if __name__ == "__main__":
    fire.Fire(main)
