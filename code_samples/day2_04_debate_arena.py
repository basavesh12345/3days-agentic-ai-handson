# =====================================================================
# Day 2 - Program 4: The AI Debate Arena ("Bull vs. Bear + The Chief Judge")
# Concept: Multi-Agent Adversarial Debate & Impartial Evaluation
# =====================================================================

import sys
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Higher temperature (0.7) encourages creative rhetoric and diverse debate angles
llm = ChatOllama(model="llama3.2", temperature=0.7)

# ── STEP 1: Define Opposing Agent Personas ──

# Agent 1: The Bull (Technological Optimist & Innovation Advocate)
bull_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are Debater A: 'The Bull' — a passionate, visionary tech optimist. Argue strongly IN FAVOR of the proposition. Keep arguments bold and concise (max 3 sentences)."),
    ("human", "{instruction}")
])

# Agent 2: The Bear (Skeptical Industry Realist & Devil's Advocate)
bear_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are Debater B: 'The Bear' — a sharp, skeptical industry critic. Argue strongly AGAINST the proposition. Keep counter-arguments punchy (max 3 sentences)."),
    ("human", "{instruction}")
])

# Agent 3: The Chief Judge (Impartial Arbitrator with Strict Rubric)
judge_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are 'The Chief Debate Judge'. Evaluate strictly on:
1. Logical consistency
2. Quality of evidence/examples
3. Counter-rebuttal strength
Provide a scorecard with scores out of 10 for both sides, then declare an official WINNER with justification."""),
    ("human", "Topic: \"{topic}\"\n\nDebate Transcript:\n{transcript}\n\nDeliver Judgement & Scorecard:")
])

# Compose LCEL chains for all three agents
bull_chain = bull_prompt | llm | StrOutputParser()
bear_chain = bear_prompt | llm | StrOutputParser()
judge_chain = judge_prompt | llm | StrOutputParser()

# ── STEP 2: Multi-Agent Message-Passing Orchestration ──
def run_debate_arena(topic: str):
    print("=" * 65)
    print(f"🥊 WELCOME TO THE AI DEBATE ARENA\n📌 TOPIC: \"{topic}\"")
    print("=" * 65)

    transcript = []

    # Round 1: Opening Statements
    print("\n[ROUND 1: OPENING STATEMENTS]")
    a_opening = bull_chain.invoke({"instruction": f"Give opening statement supporting: '{topic}'"})
    print(f"🟢 Debater A (The Bull):\n{a_opening}\n")
    transcript.append(f"Debater A Opening:\n{a_opening}\n")

    # Debater B reacts directly to Debater A's opening
    b_opening = bear_chain.invoke({"instruction": f"Give opening statement opposing '{topic}', reacting to: '{a_opening}'"})
    print(f"🔴 Debater B (The Bear):\n{b_opening}\n")
    transcript.append(f"Debater B Opening:\n{b_opening}\n")

    # Round 2: Cross-Examination & Direct Rebuttal
    print("\n[ROUND 2: REBUTTALS]")
    a_rebuttal = bull_chain.invoke({"instruction": f"Rebut Debater B's critique:\n'{b_opening}'"})
    print(f"🟢 Debater A Rebuttal:\n{a_rebuttal}\n")
    transcript.append(f"Debater A Rebuttal:\n{a_rebuttal}\n")

    b_rebuttal = bear_chain.invoke({"instruction": f"Deliver final counter-strike against: '{a_rebuttal}'"})
    print(f"🔴 Debater B Closing Rebuttal:\n{b_rebuttal}\n")
    transcript.append(f"Debater B Rebuttal:\n{b_rebuttal}\n")

    # Round 3: Chief Judge Evaluates the entire transcript
    print("=" * 65 + "\n⚖️ THE CHIEF JUDGE'S SCORECARD & VERDICT\n" + "=" * 65)
    verdict = judge_chain.invoke({"topic": topic, "transcript": "\n".join(transcript)})
    print(verdict)

if __name__ == "__main__":
    # Accept CLI argument or fallback to default controversial topic
    topic = sys.argv[1] if len(sys.argv) > 1 else "Should colleges ban AI tools like ChatGPT?"
    run_debate_arena(topic)
