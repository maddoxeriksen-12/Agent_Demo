"""
OpenAI Agent SDK Example: Custom Function Tools Agent
Demonstrates how to create and use custom function tools
"""

import asyncio
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

# Load environment variables
load_dotenv(Path(__file__).parent / '.env')


# Custom function implementations using @function_tool decorator
@function_tool
def calculator(operation: str, num1: float, num2: float) -> str:
    """Perform basic arithmetic operations (add, subtract, multiply, divide)

    Args:
        operation: The operation to perform: add, subtract, multiply, divide
        num1: First number
        num2: Second number

    Returns:
        JSON string with the calculation result
    """
    try:
        operation = operation.lower()

        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "divide":
            if num2 == 0:
                return "Error: Cannot divide by zero"
            result = num1 / num2
        else:
            return f"Error: Unknown operation '{operation}'"

        return json.dumps({
            "operation": operation,
            "num1": num1,
            "num2": num2,
            "result": result
        })
    except Exception as e:
        return f"Error: {str(e)}"


@function_tool
def get_weather(location: str, units: str = "fahrenheit") -> str:
    """Get current weather information for a location

    Args:
        location: City name or location
        units: Temperature units: fahrenheit or celsius (default: fahrenheit)

    Returns:
        JSON string with weather data
    """
    try:
        # Mock weather data
        weather_data = {
            "location": location,
            "temperature": 72 if units == "fahrenheit" else 22,
            "units": units,
            "condition": "Sunny",
            "humidity": 65,
            "wind_speed": 10
        }

        return json.dumps(weather_data)
    except Exception as e:
        return f"Error: {str(e)}"


async def run_function_tools_agent():
    """Run an agent with custom function tools"""

    # Create agent with custom function tools
    agent = Agent(
        name="Multi-Tool Assistant",
        instructions="""You are a helpful assistant with access to calculator and weather tools.
        Use the calculator tool for mathematical operations.
        Use the weather tool to provide weather information.
        Always explain your reasoning and show the results clearly.""",
        tools=[calculator, get_weather],
        model="gpt-4o"
    )

    print("Function Tools Agent initialized successfully!")
    print("Agent has calculator and weather lookup capabilities.")
    print("-" * 50)

    # Example queries to demonstrate function tools
    queries = [
        "What is 1234 multiplied by 567?",
        "Calculate 100 divided by 8, then add 50 to the result",
        "What's the weather like in San Francisco?",
        "If the temperature in New York is 72 Fahrenheit, what is that in Celsius? Use the calculator to convert."
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

    return "Function tools agent completed successfully"


if __name__ == "__main__":
    result = asyncio.run(run_function_tools_agent())
    print(f"\n{result}")
