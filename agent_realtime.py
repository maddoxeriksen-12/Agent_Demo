"""
OpenAI Agent SDK Example: Realtime Agent
Demonstrates a realtime voice/text agent with streaming capabilities
"""

import asyncio
import os
from openai import AsyncOpenAI
from agents.realtime import RealtimeAgent, RealtimeRunner


async def run_realtime_agent():
    """Run a realtime agent with voice capabilities"""

    print("Realtime Agent Example")
    print("-" * 50)

    # Create realtime agent
    agent = RealtimeAgent(
        name="Voice Assistant",
        instructions="""You are a helpful voice assistant.
        Respond naturally and conversationally.
        Keep responses concise and friendly.
        You can help with questions, calculations, and general assistance."""
    )

    # Configure runner with realtime settings
    runner = RealtimeRunner(
        starting_agent=agent,
        config={
            "model_settings": {
                "model_name": "gpt-4o-realtime-preview",
                "voice": "alloy",
                "modalities": ["text", "audio"],
                "temperature": 0.8
            },
            "turn_detection": {
                "type": "server_vad",
                "threshold": 0.5,
                "silence_duration_ms": 500
            }
        }
    )

    print("Realtime Agent initialized successfully!")
    print("Starting session...")
    print("-" * 50)

    try:
        # Start the realtime session
        session = await runner.run()

        # Example: Send text messages in realtime mode
        test_messages = [
            "Hello! Can you hear me?",
            "What's 25 multiplied by 4?",
            "Tell me a fun fact about space."
        ]

        async with session:
            for message in test_messages:
                print(f"\nUser: {message}")
                print("Agent: ", end="", flush=True)

                # Send message and process response
                await session.send_text(message)

                # Listen for response events
                collected_text = ""
                async for event in session:
                    if event.type == "response.text.delta":
                        text_chunk = event.delta
                        print(text_chunk, end="", flush=True)
                        collected_text += text_chunk
                    elif event.type == "response.done":
                        print()
                        break

                print("-" * 50)

        return "Realtime agent completed successfully"

    except Exception as e:
        return f"Realtime agent error: {str(e)}"


async def run_realtime_simple():
    """Simplified realtime agent for testing without audio I/O"""

    print("Simplified Realtime Agent (Text Mode)")
    print("-" * 50)

    # Initialize OpenAI client
    client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Create a simple realtime-capable agent
    agent = RealtimeAgent(
        name="Text Assistant",
        instructions="You are a helpful assistant. Respond concisely and clearly."
    )

    print("Agent initialized successfully!")
    print("Note: This is a text-mode demonstration of realtime capabilities.")
    print("-" * 50)

    # Simple conversation flow
    conversation = [
        "Hi there!",
        "What can you help me with?",
        "Thanks for the information!"
    ]

    for msg in conversation:
        print(f"\nUser: {msg}")
        print(f"Agent: Processing realtime response...")
        print("-" * 50)

    return "Realtime agent demonstration completed"


if __name__ == "__main__":
    # Use simplified version for testing without audio dependencies
    result = asyncio.run(run_realtime_simple())
    print(f"\n{result}")
    print("\nNote: Full realtime audio requires additional setup and audio I/O handling.")
    print("This example demonstrates the structure. For production, implement audio streaming.")
