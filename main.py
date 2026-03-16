import asyncio
import json
import os
import httpx
from typing import TypedDict, Annotated
from gradient_adk import entrypoint
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

# ==========================================
# HYBRID TOOL 1: High-Level Cloud API (MCP)
# ==========================================
@tool
async def get_cloud_report() -> str:
    """Fetches a real-time audit of all DigitalOcean resources (Droplets, Apps, DBs, Kubernetes, Domains, Spaces, etc)."""
    token = os.environ.get("DIGITALOCEAN_API_TOKEN")
    if not token: return "Error: Missing DIGITALOCEAN_API_TOKEN"
    
    # FULL MCP SCOPE
    endpoints = {
        "droplets": "https://droplets.mcp.digitalocean.com/mcp",
        "apps": "https://apps.mcp.digitalocean.com/mcp",
        "databases": "https://databases.mcp.digitalocean.com/mcp",
        "domains": "https://networking.mcp.digitalocean.com/mcp",
        "kubernetes": "https://doks.mcp.digitalocean.com/mcp",
        "accounts": "https://accounts.mcp.digitalocean.com/mcp",
        "insights": "https://insights.mcp.digitalocean.com/mcp",
        "marketplace": "https://marketplace.mcp.digitalocean.com/mcp",
        "spaces": "https://spaces.mcp.digitalocean.com/mcp"
    }
    
    # ACCURATE DO MCP TOOL MAPPINGS
    tool_map = {
        "droplets": "droplet-list",
        "apps": "apps-list",               
        "databases": "db-cluster-list",
        "domains": "domain-list",
        "kubernetes": "doks-list-clusters",
        "accounts": "account-get-information",
        "marketplace": "1-click-list",
        "spaces": "spaces-key-list"
    }
    
    async def fetch(name, url, client):
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        t_name = tool_map.get(name)
        try:
            # 1. Handshake
            await client.post(url, json={"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"do-audit","version":"1"}}}, headers=headers)
            
            # 2. Execute Tool
            resp = await client.post(url, json={"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":t_name,"arguments":{}}}, headers=headers)
            data = resp.json()
            
            # 3. Proper Error Handling (Catches the exact issue you had)
            if "error" in data:
                return name, {"error": data["error"].get("message", "Unknown RPC Error")}
                
            return name, json.loads(data["result"]["content"][0]["text"])
        except Exception as e:
            return name, {"error": str(e)}

    # Timeout bumped to 60s because 9 endpoints are being hit simultaneously
    async with httpx.AsyncClient(timeout=60.0) as client:
        results = await asyncio.gather(*(fetch(n, u, client) for n, u in endpoints.items()))
        return json.dumps(dict(results))

# ==========================================
# HYBRID TOOL 2: Local Business Logic
# ==========================================
@tool
def calculate_cloud_cost(hours: int, monthly_price: float) -> str:
    """Calculates the estimated cost of a cloud instance over a specific number of hours."""
    hourly_rate = monthly_price / 730  # Approx hours in a month
    cost = hours * hourly_rate
    return f"Estimated cost for {hours} hours is ${cost:.2f}"

# ==========================================
# LANGGRAPH STATE & MEMORY
# ==========================================
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

llm = ChatOpenAI(
    base_url="https://inference.do-ai.run/v1",
    api_key=os.environ.get("GRADIENT_MODEL_ACCESS_KEY"),
    model="openai-gpt-oss-120b"
)

tools = [get_cloud_report, calculate_cloud_cost]
llm_with_tools = llm.bind_tools(tools)

async def agent_node(state: State):
    return {"messages": [await llm_with_tools.ainvoke(state["messages"])]}

workflow = StateGraph(State)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode(tools))
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", tools_condition)
workflow.add_edge("tools", "agent")

app = workflow.compile(checkpointer=MemorySaver())

# ==========================================
# ADK DEPLOYMENT ENTRYPOINT
# ==========================================
@entrypoint
async def main(payload: dict, context: dict):
    user_prompt = payload.get("prompt") or payload.get("text") or "Hello"
    thread_id = payload.get("thread_id", "default-session")
    
    config = {"configurable": {"thread_id": thread_id}}
    
    final_state = await app.ainvoke(
        {"messages": [HumanMessage(content=user_prompt)]}, 
        config=config
    )
    
    return {"response": final_state["messages"][-1].content}
