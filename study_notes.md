# Agentic AI: Core Study Notes

These notes break down the most critical concepts you need to master to build AI Agents in Python.

## 1. Core Terminology
*   **LLM (Large Language Model):** The "brain." A stateless text-prediction engine (e.g., GPT-4o, Claude 3.5). It doesn't *do* anything on its own.
*   **Agent:** An LLM wrapped in a loop that gives it **Memory** (state), **Tools** (actions), and **Planning** (reasoning).
*   **Tool / Function Calling:** The mechanism where an LLM is given a JSON schema of available functions and can request that your code run them.
*   **State / Context:** The history of the conversation, including user prompts, tool requests, and tool results. This is how the agent "remembers" what it's doing.

## 2. The ReAct Loop (Reason + Act)
This is the fundamental loop of any agent. Master this mentally:
1.  **Observe:** User provides a task.
2.  **Think:** LLM decides if it can answer directly OR if it needs a tool.
3.  **Act:** LLM outputs a tool call request (e.g., `{"name": "search", "args": {"q": "python"}}`).
4.  **Execute (Local Code):** Python intercepts the request, runs the actual `search()` function locally.
5.  **Observe (Feedback):** Python appends the result of `search()` back to the LLM's message history.
6.  **Repeat:** Go back to Step 2 until the LLM has enough information to output a final text answer.

## 3. The Anatomy of a Tool
To give an LLM a tool, you need two things:
1.  **The Python Function:** The actual code that runs (e.g., `def query_database(sql): ...`)
2.  **The JSON Schema:** The instruction manual for the LLM. It must include:
    *   `name`: What the tool is called.
    *   `description`: **CRITICAL.** The LLM uses this to decide *when* to use the tool. Write this as if you are explaining the tool to a smart intern.
    *   `parameters`: The arguments the tool expects (types, descriptions, required fields).

## 4. Message History Rules (OpenAI Standard)
When building the loop from scratch, message order matters immensely. It must look like this:
1.  `{"role": "user", "content": "What's the weather in Tokyo?"}`
2.  `{"role": "assistant", "tool_calls": [...]}` *(The LLM asks for the tool)*
3.  `{"role": "tool", "tool_call_id": "call_123", "content": "72 degrees"}` *(You give the result)*
4.  `{"role": "assistant", "content": "It is 72 degrees in Tokyo."}` *(The final answer)*

*Note: You MUST provide the tool result back to the LLM before asking it to continue.*

## 5. Common Pitfalls to Avoid
*   **Vague Tool Descriptions:** If your tool is described as `"Gets data"`, the LLM will guess incorrectly. Use `"Fetches user profile data using a user_id string"`.
*   **Infinite Loops:** In a naive ReAct loop, the LLM might keep calling the same tool over and over if the tool returns an error or unexpected data. Always implement a `max_steps` limit in your loop.
*   **Context Window Overflow:** If your tool returns a 10,000-line JSON response, the LLM will crash or get confused. Always filter/summarize tool outputs before feeding them back to the LLM.
*   **Trusting the LLM:** Never let an LLM run destructive tools (like `DROP TABLE` or `os.system("rm -rf")`) without a "Human-in-the-Loop" approval step in your Python code.

## 6. Framework Progression
When you are ready to use frameworks, learn them in this order:
1.  **Raw API (OpenAI/Anthropic SDK):** Build the loop yourself (like in `simple_agent.py`) to understand the mechanics.
2.  **CrewAI:** Best for quickly spinning up multiple agents with distinct personas (e.g., Researcher + Writer) without worrying about complex routing.
3.  **LangGraph (The End Goal):** Use this for production. It treats the agent loop as a State Graph (nodes and edges). It gives you absolute control over infinite loops, state management, and memory.
