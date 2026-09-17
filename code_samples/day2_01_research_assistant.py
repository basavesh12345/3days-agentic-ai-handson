# =====================================================================
# Day 2 - Program 1: Personal Research Assistant Agent
# Concept: Single-Agent ReAct (Reason + Act) Loop with Tool Calling
# =====================================================================

# 1. Suppress internal deprecation warnings to keep student terminal output clean
import warnings
warnings.filterwarnings("ignore")

import math
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langgraph.prebuilt import create_react_agent

# ── STEP 1: Define Custom Python Tools ──
# The @tool decorator automatically generates JSON Schema from docstring and type hints.
# The LLM reads the docstring to understand WHEN and HOW to call the tool.
@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression safely.
    Use this for any calculations. Input: math expression as string.
    Examples: '25 * 4', 'math.sqrt(256)', '(100 + 200) / 3'"""
    try:
        # Safely restrict globals to prevent arbitrary system commands
        result = eval(expression, {"__builtins__": {}}, {"math": math})
        return f"Result: {result}"
    except Exception as e:
        return f"Error in calculation: {str(e)}"

# ── STEP 2: Initialize External Search & Reference Tools ──
# Limit Wikipedia characters to prevent overwhelming local model context window
wiki_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=1000)
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)
search_tool = DuckDuckGoSearchRun()

# Pack all tools into a list to provide to the agent
tools = [search_tool, wiki_tool, calculator]

# ── STEP 3: Initialize Local LLM & ReAct Agent ──
# temperature=0 ensures deterministic, hallucination-free tool selection
llm = ChatOllama(model="llama3.2", temperature=0)

# create_react_agent binds tools to the LLM and manages the Reason -> Act -> Observe loop
agent = create_react_agent(llm, tools)

# ── STEP 4: Interactive User Loop ──
def main():
    print("🔬 Personal Research Assistant Agent")
    print("=" * 50)
    print("Tools available: Web Search (DuckDuckGo), Wikipedia, Math Calculator")
    print("Type 'quit' or 'exit' to stop.\n")
    
    while True:
        query = input("🧑 You: ").strip()
        if query.lower() in ['quit', 'exit']:
            print("👋 Goodbye!")
            break
        if not query:
            continue
        
        print("\n🤖 Agent working...\n")
        # Invoke agent by passing user prompt in standard messages format
        result = agent.invoke({"messages": [("user", query)]})
        
        # The final response is the content of the last message in the agent's state
        print(f"\n✅ Final Answer:\n{result['messages'][-1].content}")
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    main()
