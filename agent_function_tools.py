"""
OpenAI Agent SDK Example: Custom Function Tools Agent
Demonstrates how to create and use custom function tools
"""

import asyncio
import os
import json
from typing import Dict, Any
from openai import AsyncOpenAI
from agents import Agent, Runner
from agents.tools import FunctionTool, ToolContext
from pydantic import BaseModel, Field


# Define a Pydantic model for structured arguments
class CalculatorArgs(BaseModel):
    """Arguments for calculator operations"""
    operation: str = Field(description="The operation to perform: add, subtract, multiply, divide")
    num1: float = Field(description="First number")
    num2: float = Field(description="Second number")


class WeatherArgs(BaseModel):
    """Arguments for weather lookup"""
    location: str = Field(description="City name or location")
    units: str = Field(default="fahrenheit", description="Temperature units: fahrenheit or celsius")


# Custom function implementations
async def calculator_function(ctx: ToolContext, args: str) -> str:
    """Perform basic calculator operations"""
    try:
        parsed_args = CalculatorArgs.model_validate_json(args)

        num1 = parsed_args.num1
        num2 = parsed_args.num2
        operation = parsed_args.operation.lower()

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


async def get_weather(ctx: ToolContext, args: str) -> str:
    """Simulate getting weather information (mock function)"""
    try:
        parsed_args = WeatherArgs.model_validate_json(args)

        # Mock weather data
        weather_data = {
            "location": parsed_args.location,
            "temperature": 72 if parsed_args.units == "fahrenheit" else 22,
            "units": parsed_args.units,
            "condition": "Sunny",
            "humidity": 65,
            "wind_speed": 10
        }

        return json.dumps(weather_data)
    except Exception as e:
        return f"Error: {str(e)}"


async def run_function_tools_agent():
    """Run an agent with custom function tools"""

    # Initialize OpenAI client
    client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Create custom function tools
    calculator_tool = FunctionTool(
        name="calculator",
        description="Perform basic arithmetic operations (add, subtract, multiply, divide)",
        params_json_schema=CalculatorArgs.model_json_schema(),
        on_invoke_tool=calculator_function
    )

    weather_tool = FunctionTool(
        name="get_weather",
        description="Get current weather information for a location",
        params_json_schema=WeatherArgs.model_json_schema(),
        on_invoke_tool=get_weather
    )

    # Create agent with custom function tools
    agent = Agent(
        name="Multi-Tool Assistant",
        instructions="""You are a helpful assistant with access to calculator and weather tools.
        Use the calculator tool for mathematical operations.
        Use the weather tool to provide weather information.
        Always explain your reasoning and show the results clearly.""",
        tools=[calculator_tool, weather_tool],
        model="gpt-4o"
    )

    # Create runner
    runner = Runner(client=client, agent=agent)

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
        async with runner.run_stream(query) as stream:
            async for chunk in stream.text_stream():
                print(chunk, end="", flush=True)

        print("\n" + "-" * 50)

    return "Function tools agent completed successfully"


if __name__ == "__main__":
    result = asyncio.run(run_function_tools_agent())
    print(f"\n{result}")
