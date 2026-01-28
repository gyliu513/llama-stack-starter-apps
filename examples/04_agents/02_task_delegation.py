#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.
import os

import fire
from termcolor import colored

from examples.client_tools.calculator import calculator
from examples.client_tools.ticker_data import get_ticker_data
from examples.client_tools.web_search import WebSearchTool
from llama_stack_client import Agent, AgentEventLogger, LlamaStackClient

from .utils import can_model_chat, check_model_is_available, get_any_available_chat_model


def _resolve_web_tool():
    api_key = ""
    engine = "tavily"
    if "TAVILY_SEARCH_API_KEY" in os.environ:
        api_key = os.getenv("TAVILY_SEARCH_API_KEY")
    elif "BRAVE_SEARCH_API_KEY" in os.environ:
        api_key = os.getenv("BRAVE_SEARCH_API_KEY")
        engine = "brave"
    else:
        print(
            colored(
                "Warning: TAVILY_SEARCH_API_KEY or BRAVE_SEARCH_API_KEY is not set; web tool disabled.",
                "yellow",
            )
        )
        return None
    return WebSearchTool(engine, api_key)


def _route_prompt(prompt: str, web_available: bool) -> str:
    lower_prompt = prompt.lower()
    if any(token in lower_prompt for token in ["stock", "ticker", "price", "market"]):
        return "finance"
    if any(token in lower_prompt for token in ["calculate", "sum", "+", "-", "*", "/"]):
        return "math"
    if any(token in lower_prompt for token in ["search", "latest", "who", "when", "news", "find"]):
        return "research" if web_available else "general"
    return "general"


def main(host: str, port: int, model_id: str | None = None):
    client = LlamaStackClient(base_url=f"http://{host}:{port}")

    if model_id is None:
        model_id = get_any_available_chat_model(client)
        if model_id is None:
            return
    else:
        if not check_model_is_available(client, model_id):
            return
        if not can_model_chat(client, model_id):
            print(
                colored(
                    f"Model `{model_id}` does not support chat. Choose a chat-capable model.",
                    "red",
                )
            )
            return

    web_tool = _resolve_web_tool()
    web_available = web_tool is not None

    agents = {
        "general": Agent(
            client,
            model=model_id,
            instructions="You are a helpful assistant.",
        ),
        "research": Agent(
            client,
            model=model_id,
            instructions="You are a research assistant. Use web search when helpful.",
            tools=[web_tool] if web_tool is not None else [],
        ),
        "math": Agent(
            client,
            model=model_id,
            instructions="You are a math assistant. Use tools for calculations.",
            tools=[calculator],
        ),
        "finance": Agent(
            client,
            model=model_id,
            instructions="You are a finance assistant. Use tools for ticker data.",
            tools=[get_ticker_data],
        ),
    }

    sessions = {name: agent.create_session(f"task-delegation-{name}") for name, agent in agents.items()}

    user_prompts = [
        "Summarize what Llama Stack provides in one sentence.",
        "What is the closing price of GOOG for 2023?",
        "Calculate (45 * 18) / 6.",
        "Search for the latest Llama Stack release notes and summarize them.",
    ]

    for prompt in user_prompts:
        route = _route_prompt(prompt, web_available)
        agent = agents[route]
        session_id = sessions[route]
        print(colored(f"[router] {prompt} -> {route}", "cyan"))
        response = agent.create_turn(
            messages=[{"role": "user", "content": prompt}],
            session_id=session_id,
        )
        for printable in AgentEventLogger().log(response):
            print(printable, end="", flush=True)


if __name__ == "__main__":
    fire.Fire(main)
