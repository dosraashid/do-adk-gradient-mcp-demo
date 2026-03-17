# 🤖 DigitalOcean ADK + MCP + LangGraph + Context: DevOps Agent Demo

This repository demonstrates the **"Golden Path"** for building a fully-managed AI agent built on the DigitalOcean Gradient™ AI Platform. This agent uses LangGraph for state management, features checkpointer-style memory persistence, and includes an embedded Model Context Protocol (MCP) tool to securely audit a DigitalOcean infrastructure environment.

---

## Architecture Highlights
* **Agent Framework**: LangGraph (`StateGraph`, `ToolNode`)
* **Deployment**: DigitalOcean Gradient™ AI ADK (`@entrypoint`)
* **Inference**: Gradient™ AI Platform using `openai-gpt-oss-120b`
* **Memory**: Persistent thread isolation using `MemorySaver()`.

---

## 🏗️ Project Structure & File Guide

A production-ready architecture designed for the DigitalOcean Gradient™ AI Platform, featuring a self-contained LangGraph agent with dynamic MCP tool discovery and stateful memory persistence.

```text
/do-adk-gradient-mcp-demo
└── .gradient/            # ⚙️ Gradient™ AI Configuration Folder
    └── agent.yml         # 🚀 Deployment Metadata & Routing Config
├── .env                  # 🔑 Local API keys (Never committed to Git)
├── .gitignore            # 🛡️ Security: Prevents sensitive keys from leaking
├── README.md             # 📝 Detailed Project Documentation
├── main.py               # 🧠 The Brain, Hands, and Memory (All-in-One Orchestrator)
└── requirements.txt      # 📦 Python dependency manifest
```

---

## 🔍 Detailed File Breakdown

### ⚙️ `.gradient/agent.yml`
**The Manifest.** This file acts as the "identity card" for your agent. It tells the DigitalOcean Gradient™ platform how to handle your code. It defines the agent’s name, description, and critically, the **entrypoint**—telling the cloud environment exactly which function in `main.py` to execute when a request is received.

### 🔑 `.env`
**The Vault.** A local-only file used to store sensitive credentials like your `DIGITALOCEAN_API_TOKEN` and `GRADIENT_MODEL_ACCESS_KEY`. The code loads these variables at runtime so the agent can talk to your infrastructure securely.

### 🛡️ `.gitignore`
**The Shield.** A vital security configuration that ensures your private secrets stay private. It tells Git to ignore the `.env` file and temporary Python artifacts, preventing accidental leaks of your API keys to public repositories.

### 📝 `README.md`
**The Blueprint.** The central documentation for the project. It explains the "why" and "how" of the architecture, providing the necessary commands for others to clone, initialize, and deploy the agent.

### 🧠 `main.py`
**The Orchestrator.** This is the core engine of your application, combining three critical AI patterns into a single file to create a functional autonomous agent:
* **The Brain:** It acts as the decision-maker, analyzing user intent to determine when to pull live data or perform local calculations.
* **The Hands:** Implements a robust **MCP (Model Context Protocol) Client**. It handles the complex two-step JSON-RPC "handshake" (Initialize + Call) across 9 distinct DigitalOcean service endpoints using your verified `tool_map` for 100% accuracy.
* **The Memory:** Utilizes LangGraph's **`MemorySaver`** checkpointer. This enables "Session-Aware" intelligence, where the agent stores the entire state of the conversation (including previous tool outputs) under a unique `thread_id` for seamless follow-up questions.

### 📦 `requirements.txt`
**The Ecosystem.** This file manifest ensures the cloud environment is identical to your local setup. It lists the essential libraries,ensuring they are pre-installed in the agent's secure container.

---

# ✨ Key Capabilities

| Capability | Description |
|---|---|
| **Managed Conversation History** | Implements LangGraph `MemorySaver` persistence. The agent retains full state, including tool outputs and LLM reasoning steps, enabling context-aware follow-ups and session resumes via `thread_id`. |
| **Comprehensive MCP Mapping** | Hardcoded, validated tool mappings for the DigitalOcean MCP ecosystem. Ensures reliable execution of specific commands like `apps-list` and `db-cluster-list` across 9 different cloud services. |
| **Thread Isolation** | Provides strict logical isolation for user sessions. Using the `configurable` thread pattern ensures that conversation history from one session never leaks into another. |
| **Hybrid Tooling Architecture** | Demonstrates the power of mixing remote Cloud APIs (via MCP over HTTP) with local business logic (Python `@tool` functions) within a single unified reasoning loop. |
| **Standardized Telemetry** | All interactions follow the LangGraph `ToolNode` semantics, providing clean traces and making it simple to monitor exactly when and why a specific cloud service was queried. |

---

# 🚀 Recommended "Wow" Tests

Use these prompts to showcase the unique capabilities of your **MCP + LangGraph Agent**. These tests are specifically designed around the exact `list` and `get-information` endpoints available in the agent's toolset.

| Feature Highlight | Goal | Prompt Payload |
|---|---|---|
| **Full Infrastructure Audit** | Multi-service retrieval | "Give me a full report of my account. List my droplets, my apps, and any active databases." |
| **Account & Marketplace** | Metadata Access | "Fetch my account information (like my email or droplet limit). Then list 5 available Marketplace 1-click apps I could install." |
| **Cross-Session Memory** | Stateful Context | **Step 1:** "Remember that 'nyc3' is my preferred deployment region." <br> **Step 2:** "Based on our last message, do I have any active resources in my preferred region?" |
| **Hybrid Tooling (Math)** | Local Logic Execution | "Assume I plan to spin up a new $40/month resource. Use your local cost tool to calculate exactly how much it will cost to run for 120 hours." |
| **Security & Networking** | Specific MCP Tooling | "Check my account for any configured Domains and tell me if I have any active Spaces access keys." |
| **Thread Isolation Test** | Multi-Tenancy Security | **Session A (`thread_id: "prod-env"`):** "Scan my account for Droplets with 'prod' in the name. Remember these are mission-critical." <br> **Session B (`thread_id: "dev-env"`):** "Which servers did we identify as mission-critical?" (The agent should not know it in Session B). |

---

# 🚀 Setup & Installation

### 1. Prerequisites
- **Python 3.12** recommended for the latest LangGraph and Asyncio features.
- **DigitalOcean API Token**: Needs `read` permissions for resources and `create`, `read` and `update` scopes on `genai`. [Generate API Token here](https://cloud.digitalocean.com/account/api/tokens).
- **Gradient™ Model Access Key**: Required to access the Serverless Inference endpoint for local testing. [Generate Model Access Key here](https://cloud.digitalocean.com/gen-ai/model-access-keys).

### 2. Environment Setup

Install the required Python dependencies:

```bash
git clone https://github.com/dosraashid/do-adk-gradient-mcp-demo
cd do-adk-gradient-mcp-demo
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configuration & Credentials

Update the `.env` file in the root directory. This file is used to authenticate your local session and the cloud-hosted agent.

```bash
# .env

# Used for local testing and to authenticate your session with Serverless Inference engine.
GRADIENT_MODEL_ACCESS_KEY="your_model_access_key"

# Used for agent deployment and to authorize the toolset to audit your DO infrastructure.
# (Requires GenAI Create, Read and Update scopes).
DIGITALOCEAN_API_TOKEN="your_DO_token"
```

Make sure .env is listed in your .gitignore to prevent accidental exposure of secrets.

### 4. Initialization

Before running the agent for the first time, you must initialize the Gradient™ configuration:

```bash
gradient agent init
```

When prompted:

* Agent workspace name: Give it any random name, for example, `Auditor`.
* Agent deployment name: Set this to `main`.

### 5. Run

Start the agent server locally using the Gradient™ ADK:

```bash
gradient agent run
```

This will spin up a local Uvicorn server (typically on `http://localhost:8080`). Once it is running, you can issue prompts to the system in a separate terminal tab using `curl`. 

By passing a `thread_id` in your JSON payload, you tell the agent which "save slot" to use, allowing it to maintain conversational memory across multiple requests.

```bash
curl -X POST http://localhost:8080/run \
     -H "Content-Type: application/json" \
     -d '{
           "prompt": "List my DigitalOcean apps.",
           "thread_id": "my-dev-session-1"
         }'
```

### 6. Deployment

Once you have verified the agent's behavior locally, you can deploy it to the DigitalOcean Gradient™ AI Platform cloud. This transforms your local code into a managed, serverless endpoint.

```bash
export $(cat .env | xargs)
gradient agent deploy
```

#### Interacting with the Cloud Agent

Once the deployment is successful, you can interact with your agent using a curl command.

```bash
curl -X POST $AGENT_ENDPOINT \
    -H "Authorization: Bearer $DIGITALOCEAN_API_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
          "prompt": "List my droplets.",
          "thread_id": "production-audit-1"
        }'
```

Finding your AGENT_ENDPOINT: This URL is printed in your terminal immediately after the deploy command finishes. You can also retrieve it at any time from the DigitalOcean Cloud Panel under the Gradient™ AI Platform page.

**Important: Authorization Token**

The $DIGITALOCEAN_API_TOKEN used in the header must be a Personal Access Token with `read` permissions. [Generate API Token here](https://cloud.digitalocean.com/account/api/tokens). This ensures the request is authorized to trigger the agent's inference engine and execute the underlying MCP tools.

---

## 🧪 Verification Commands & Test Cases

This agent uses **Thread-Scoped Persistence** via LangGraph Checkpointers. Run these test cases in sequence in your terminal to verify that memory is isolated between sessions, and that the agent can seamlessly route between cloud (MCP) and local tools.

| Test Case | Purpose | Terminal Command (`curl`) | Expected Behavior |
| :--- | :--- | :--- | :--- |
| **1. Establish Context** | Fetch cloud data & save to Thread A. | `{"prompt": "List my DigitalOcean droplets.", "thread_id": "alpha"}` | Agent triggers `droplet-list` via the MCP handshake and returns your active droplets. |
| **2. Test Reasoning** | Verify the agent can analyze previously fetched data. | `{"prompt": "Based on that list, which Droplet was created first?", "thread_id": "alpha"}` | Agent retrieves the previous tool output from memory and identifies the specific resource. |
| **3. Verify Context Recall** | Test exact conversation history recall in same thread. | `{"prompt": "What was the very first question I asked you?", "thread_id": "alpha"}` | Checkpointer retrieves the history; agent accurately replies that you asked to list droplets. |
| **4. Test Thread Isolation** | Prove memory is strictly scoped and isolated. | `{"prompt": "What was the very first question I asked you?", "thread_id": "beta"}` | Agent looks at the isolated `beta` thread, sees no history, and treats this as a brand-new conversation. |

---

## 🏗 Architecture: The Hybrid Runtime

This agent implements a production-grade reasoning loop for DevOps automation, bridging the gap between local logic and the DigitalOcean cloud ecosystem.

1. **Stateful Orchestration (LangGraph):** Uses a `StateGraph` to manage a circular reasoning loop. It ensures a structured flow where the LLM decides to act, the `ToolNode` executes the action, and the results are fed back for final synthesis.
2. **Managed Persistence (MemorySaver):** Implements `MemorySaver` to provide checkpointer-style persistence. By using a `thread_id`, the agent maintains isolated "memory buckets" for different sessions, allowing it to remember past infrastructure audits without leaking data between users.
3. **The "Brain" (Llama 3 via Gradient™):** Routes complex reasoning to **Llama 3** using the `ChatOpenAI` client. By targeting the DigitalOcean Inference gateway, it leverages frontier-model intelligence while keeping data within the DO ecosystem.
4. **Hybrid Tooling Logic:**
   * **Remote MCP (Cloud):** Connects to 9+ DigitalOcean services via a manual JSON-RPC handshake over HTTP. This bypasses the need for local subprocesses and interacts directly with the MCP service endpoints.
   * **Local Logic (Python):** Executes native Python code for calculations (like the `calculate_cloud_cost` tool), demonstrating how to mix cloud data with private business logic.
5. **Standardized Execution (ToolNode):** Uses the official `ToolNode` pattern. This ensures that every cloud interaction, from listing Droplets to checking Kubernetes clusters, is recorded in the message history for a transparent audit trail.

---

# 🛠️ Troubleshooting & Configuration

### 🌐 No Node.js Required
Unlike standard MCP implementations, this agent uses a **Direct HTTP Handshake** via `httpx`. This means you do **not** need Node.js or `npx` installed. The agent communicates directly with DigitalOcean’s cloud-hosted MCP endpoints.

### 🔑 Environment Secrets
Ensure your `.env` file is in the root directory and contains the following:

* **DIGITALOCEAN_API_TOKEN:** Requires **GenAI** `create`, `read`, `update` scopes. This is used by the agent to perform the handshake and fetch your infrastructure data.
* **GRADIENT_MODEL_ACCESS_KEY:** Required to authenticate your Serverless Inference calls to the model via the Gradient™ AI gateway.

### ⚠️ Common Errors
* **JSON-RPC Error:** If a tool returns an "Unknown RPC Error," check your `DIGITALOCEAN_API_TOKEN`. This usually happens if the token lacks the specific scope for the service you are trying to audit (e.g., trying to list Databases without Database Read permissions).
* **Timeout (60s):** The agent audits 9+ services simultaneously. If your account has a very large number of resources, you may need to increase the `timeout` value in the `httpx.AsyncClient` inside `main.py`.
* **401 Unauthorized:** Ensure your `GRADIENT_MODEL_ACCESS_KEY` is active and that you have exported your environment variables (`export $(cat .env | xargs)`) before running `gradient agent run`.

---

# 🤝 Contributing
This is a demo of the **Stateful MCP Architecture**. If you'd like to extend the agent's capabilities:

1. **Add Local Tools:** Add more Python functions with the `@tool` decorator in `main.py` to handle custom business logic or calculations.
2. **Expand MCP Scope:** Update the `tool_map` and `endpoints` dictionaries in `main.py` to include new DigitalOcean MCP features as they are released.
3. **Advanced Persistence:** The current setup uses `MemorySaver` (In-memory). For production use cases, you can swap this for `PostgresSaver` in LangGraph to enable long-term, database-backed conversation history.
