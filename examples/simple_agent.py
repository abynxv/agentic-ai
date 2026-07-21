import json
import os

# NOTE: You will need to install the openai package: pip install openai
# and set your OPENAI_API_KEY environment variable.
from openai import OpenAI

# ---------------------------------------------------------
# 1. Define the Tools (Functions) the agent can use
# ---------------------------------------------------------
def get_weather(location: str) -> str:
    """A mock function to get weather."""
    print(f"  [Tool Executing] -> get_weather({location})")
    # In a real app, you would call an actual weather API here.
    if "tokyo" in location.lower():
        return "It is currently 72 degrees and sunny in Tokyo."
    elif "london" in location.lower():
        return "It is currently 55 degrees and raining in London."
    else:
        return f"Weather data not found for {location}, but let's assume it's nice."

def calculate(expression: str) -> str:
    """A simple calculator using Python's eval."""
    print(f"  [Tool Executing] -> calculate({expression})")
    try:
        # Warning: eval() is dangerous in production without sanitization. 
        # This is just for demonstration.
        result = str(eval(expression))
        return result
    except Exception as e:
        return f"Error evaluating expression: {e}"

# ---------------------------------------------------------
# 2. Map tool names to actual Python functions
# ---------------------------------------------------------
AVAILABLE_TOOLS = {
    "get_weather": get_weather,
    "calculate": calculate
}

# ---------------------------------------------------------
# 3. Define the Tool Schemas (so the LLM knows what they do)
# ---------------------------------------------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression to evaluate, e.g. '2 + 2' or '10 * 5'",
                    }
                },
                "required": ["expression"],
            },
        }
    }
]

# ---------------------------------------------------------
# 4. The Agent Loop (ReAct paradigm)
# ---------------------------------------------------------
def run_agent(user_query: str):
    print(f"\nUser: {user_query}")
    print("-" * 50)
    
    client = OpenAI() # Make sure OPENAI_API_KEY is in your environment
    
    # Initialize the conversation history
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant. You have access to tools to calculate math and check the weather. Use them when needed."},
        {"role": "user", "content": user_query}
    ]

    # The Loop: The agent can take multiple steps to solve the problem
    while True:
        # Step 1: Ask the LLM what to do
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Or gpt-3.5-turbo
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        
        # Step 2: Check if the LLM wants to call a tool
        if response_message.tool_calls:
            # Add the assistant's request to call a tool into history
            messages.append(response_message)
            
            # Step 3: Execute all requested tools
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"[Agent Thinking] -> Needs to use tool: {function_name}")
                
                # Execute the actual Python function
                function_to_call = AVAILABLE_TOOLS.get(function_name)
                if function_to_call:
                    function_response = function_to_call(**function_args)
                    
                    # Step 4: Give the tool's result back to the LLM
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": str(function_response),
                    })
                else:
                    print(f"Error: Tool {function_name} not found.")
            
            # The loop will now go back to Step 1, sending the tool results to the LLM
            # so it can figure out if it has enough info to give a final answer.
            
        else:
            # No tool calls were requested, the LLM is giving its final answer.
            print(f"\n[Agent Final Answer]: {response_message.content}")
            break

# ---------------------------------------------------------
# 5. Run it!
# ---------------------------------------------------------
if __name__ == "__main__":
    # Test 1: Needs the calculator tool
    run_agent("What is 250 times 14?")
    
    # Test 2: Needs the weather tool
    run_agent("What's the weather like in Tokyo right now?")
    
    # Test 3: Needs BOTH tools (multi-step reasoning)
    run_agent("If the temperature in London doubles, what would the new temperature be? Give me the math.")
