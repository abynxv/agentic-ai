# AutoResearcher API 🚀

An autonomous AI research agent wrapped in a production-ready FastAPI web service.

Given a topic, the AutoResearcher uses a ReAct (Reasoning + Acting) loop to search the live internet, read multiple sources, and compile a comprehensive, well-structured Markdown report. It demonstrates the core mechanics of Agentic AI without relying on heavy frameworks like LangChain or CrewAI.

## ✨ Features
*   **Agentic ReAct Loop**: Built from scratch using the OpenAI API.
*   **Live Web Browsing**: Uses `duckduckgo-search` to find up-to-date information for free.
*   **FastAPI Backend**: Ready to be connected to any frontend (React, Next.js, etc.).
*   **Swagger UI**: Auto-generated interactive API documentation.

## 📂 Project Structure
```text
.
├── agent.py               # The core ReAct loop and LLM logic
├── docs/                  # Educational materials and notes on Agentic AI
│   ├── learning_agentic_ai.md
│   └── study_notes.md
├── examples/              # Simple standalone scripts for learning
│   └── simple_agent.py
├── main.py                # FastAPI server and endpoint definitions
├── requirements.txt       # Project dependencies
└── research_tool.py       # The DuckDuckGo search tool definition and schema
```

## 🛠️ Installation

1. **Clone the repository (or navigate to the directory)**
2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your OpenAI API Key:**
   The agent requires an OpenAI key to function. Set it as an environment variable in your terminal:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

## 🚀 Usage

### 1. Start the Server
Run the FastAPI application using Uvicorn:
```bash
python main.py
```
*The server will start running on `http://0.0.0.0:8000`*

### 2. Test the API (via cURL)
Open a new terminal tab and send a POST request with a topic:
```bash
curl -X POST "http://localhost:8000/api/research" \
     -H "Content-Type: application/json" \
     -d '{"topic": "Latest advancements in solid state batteries 2024"}'
```

### 3. Test the API (via Swagger UI)
Because the project uses FastAPI, you get beautiful interactive documentation for free.
1. Make sure the server is running.
2. Open your web browser and go to: [http://localhost:8000/docs](http://localhost:8000/docs)
3. Click on the `POST /api/research` endpoint.
4. Click **"Try it out"**, enter a topic, and click **"Execute"**.

## 🧠 How it Works Under the Hood
1. The user sends a topic to the `/api/research` endpoint.
2. `main.py` passes the topic to the `run_agent()` function in `agent.py`.
3. The LLM is prompted with the topic and given the `search_web` tool schema.
4. The LLM enters a loop: it asks to search DuckDuckGo, the Python script executes the search locally, and the results are fed back to the LLM.
5. Once the LLM has enough context, it breaks the loop, synthesizes the data, and returns the final Markdown report as a JSON response.
