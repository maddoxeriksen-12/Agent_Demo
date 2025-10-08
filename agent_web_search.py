"""
OpenAI Agent SDK Example: Web Search Tool Agent
Demonstrates an agent running in a loop with web search capabilities
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from agents import Agent, Runner, WebSearchTool

# Load environment variables
load_dotenv(Path(__file__).parent / '.env')


async def run_web_search_agent():
    """Run an agent with web search capabilities in a loop"""

    # Create agent with web search tool
    agent = Agent(
        name="Research Assistant",
        instructions="""You are a helpful research assistant with web search capabilities.
        When users ask questions, search the web to find current and accurate information.
        Always cite your sources and provide comprehensive answers.""",
        tools=[WebSearchTool()],
        model="gpt-4o"
    )

    print("Web Search Agent initialized successfully!")
    print("Agent will answer questions using web search.")
    print("-" * 50)

    # Example queries to demonstrate the agent
    queries = [
        "What are the latest developments in AI agents in 2025?",
        "What is the current weather in San Francisco?",
        "Explain quantum computing breakthroughs from the last year"
    ]

    for query in queries:
        print(f"\nUser: {query}")
        print("Agent: ", end="", flush=True)

        # Run agent with streaming
        result = Runner.run_streamed(starting_agent=agent, input=query)
        async for event in result.stream_events():
            if event.type == 'raw_response_event':
                if hasattr(event, 'data') and event.data.__class__.__name__ == 'ResponseTextDeltaEvent':
                    if hasattr(event.data, 'delta'):
                        print(event.data.delta, end="", flush=True)

        print("\n" + "-" * 50)

    return "Web search agent completed successfully"


if __name__ == "__main__":
    result = asyncio.run(run_web_search_agent())
    print(f"\n{result}")
