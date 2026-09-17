# =====================================================================
# Day 2 - Program 2: The AI Fact-Checker & Web Detective
# Concept: Domain-Specific Agent with Enforced Reporting Structure
# =====================================================================

# 1. Suppress internal deprecation notices
import warnings
warnings.filterwarnings("ignore")

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
import wikipedia

# ── STEP 1: Resilient Search & Encyclopedia Tools ──
# Pro-Tip for Local LLMs: We use parameter name `topic` instead of `query`
# because small 3B models can confuse the word 'query' with internal schema tokens.
@tool
def search_web(topic: str) -> str:
    """Searches the live web for breaking news, claims, and articles."""
    # Defensive type check: unwrap dictionary if local model passed JSON object
    if isinstance(topic, dict):
        topic = str(list(topic.values())[0])
    try:
        search = DuckDuckGoSearchRun()
        return search.run(str(topic))
    except Exception as e:
        return f"Web search notice: {e}"

@tool
def lookup_wikipedia(topic: str) -> str:
    """Looks up encyclopedic facts, biographies, and history on Wikipedia."""
    if isinstance(topic, dict):
        topic = str(list(topic.values())[0])
    try:
        # Set custom user agent required by Wikimedia foundation policy
        wikipedia.set_user_agent("AgenticAIWorkshop/1.0 (student-workshop)")
        return wikipedia.summary(str(topic), sentences=3)
    except Exception as e:
        return f"Wikipedia notice: {e}"

tools = [search_web, lookup_wikipedia]

# ── STEP 2: Detective Persona & Structured Output Prompt ──
# Enforcing structured sections ensures the agent always provides a clean, audit-ready verdict
system_prompt = """You are an elite AI Fact-Checker and Investigative Journalist.
Your job is to verify or debunk claims using your web search and Wikipedia tools.

Always conclude with this EXACT format:
⚖️ VERDICT: [TRUE / FALSE / MISLEADING / UNVERIFIED]
🎯 CONFIDENCE: [HIGH / MEDIUM / LOW]
📝 FACT-CHECK SUMMARY: (2-3 concise sentences explaining the evidence)
🔗 EVIDENCE & SOURCES: (Cite specific verified facts and sources)"""

# Initialize local Llama 3.2 model
llm = ChatOllama(model="llama3.2", temperature=0)
agent = create_react_agent(llm, tools, prompt=system_prompt)

# ── STEP 3: Verification Runner Function ──
def verify_claim(claim: str):
    print(f"\n🔍 Investigating Claim: \"{claim}\"")
    print("⏳ Gathering evidence from live web & Wikipedia...\n")
    # Agent reasons over evidence and generates the structured report
    response = agent.invoke({"messages": [("user", f"Fact-check this claim: {claim}")]})
    verdict = response["messages"][-1].content
    print("=" * 60)
    print("📋 FACT-CHECK REPORT")
    print("=" * 60)
    print(verdict)
    print("=" * 60 + "\n")
    return verdict

def main():
    print("🕵️ AI Fact-Checker & Web Detective")
    print("=" * 50)
    print("Submit any viral news, tech rumor, or trivia to verify.")
    print("Type 'quit' or 'exit' to stop.\n")

    while True:
        try:
            claim = input("🔎 Enter claim to verify: ").strip()
        except EOFError:
            claim = "does ai take developers job?"
            verify_claim(claim)
            break

        if claim.lower() in ['quit', 'exit']:
            print("👋 Detective signing off!")
            break
        if not claim:
            continue

        verify_claim(claim)

if __name__ == "__main__":
    main()
