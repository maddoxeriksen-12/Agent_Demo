"""
OpenAI Agent SDK Example: Streaming Agent
Demonstrates an agent with streaming text responses
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from agents import Agent, Runner

# Load environment variables
load_dotenv(Path(__file__).parent / '.env')


async def run_realtime_simple():
    """Run an agent with streaming capabilities"""

    print("Streaming Agent Example")
    print("-" * 50)

    # Create agent with streaming
    agent = Agent(
        name="Streaming Assistant",
        instructions="""You are a helpful assistant that responds with streaming text.
        Respond naturally and conversationally.
        Keep responses concise and friendly.
        You can help with questions, calculations, and general assistance.""",
        model="gpt-4o"
    )

    print("Streaming Agent initialized successfully!")
    print("Demonstrating real-time streaming responses...")
    print("-" * 50)

    # Example queries to demonstrate streaming
    queries = [
        "Hello! Tell me about yourself.",
        "What's 25 multiplied by 4?",
        "Tell me a fun fact about space."
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

    return "Streaming agent demonstration completed"


if __name__ == "__main__":
    # Use simplified version for testing without audio dependencies
    result = asyncio.run(run_realtime_simple())
    print(f"\n{result}")
    print("\nNote: Full realtime audio requires additional setup and audio I/O handling.")
    print("This example demonstrates the structure. For production, implement audio streaming.")
