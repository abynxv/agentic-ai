import json
import json
import os
from openai import OpenAI
from research_tool import search_web, search_tool_schema

def run_agent(topic: str):
    print(f"\nInitializing Automated Researcher for topic: {topic}")
    print("=" * 60)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Please set it by running: export OPENAI_API_KEY='your_api_key'")
        return

    client = OpenAI()
    
    # System prompt defining the agent's behavior
    system_prompt = """
    You are an expert Research AI Assistant. 
    Your goal is to write comprehensive, accurate, and well-structured Markdown reports based on user topics.
    You MUST use the `search_web` tool to gather up-to-date information before writing the report.
    You can use the tool multiple times if you need to research different angles of the topic.
    
    When writing the final report:
    1. Structure it clearly with headings and bullet points.
    2. Include a "References" section at the bottom citing the URLs you found.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Please research the following topic and write a detailed markdown report: {topic}"}
    ]
    
    tools = [search_tool_schema]
    
    print("Agent is thinking...")
    
    # The ReAct Loop
    step_count = 0
    max_steps = 10 # Prevent infinite loops
    
    while step_count < max_steps:
        step_count += 1
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        
        # Check if the LLM wants to call a tool
        if response_message.tool_calls:
            # Add the request to history
            messages.append(response_message)
            
            # Execute all requested tools
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                
                if function_name == "search_web":
                    function_args = json.loads(tool_call.function.arguments)
                    query = function_args.get("query")
                    
                    # Run our custom Python function
                    tool_result = search_web(query)
                    
                    # Feed the result back to the LLM
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": tool_result,
                    })
        else:
            # No tool calls means the agent is done and has our final report
            final_report = response_message.content
            print("\n[Agent Finished Research]")
            return final_report
            
    if step_count >= max_steps:
        print("\nAgent reached maximum steps without finishing the report.")
        return "Error: Agent reached maximum steps."
