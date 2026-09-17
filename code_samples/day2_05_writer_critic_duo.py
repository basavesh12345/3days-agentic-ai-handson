# =====================================================================
# Day 2 - Program 5: The Writer & Strict Editor Feedback Loop (Reflective Duo)
# Concept: Evaluator-Optimizer Multi-Agent Quality Convergence Loop
# =====================================================================

import re, sys
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Balanced temperature (0.5) allows creative drafting while maintaining focus
llm = ChatOllama(model="llama3.2", temperature=0.5)

# ── STEP 1: Define Generator & Evaluator Personas ──

# Agent 1: The Creator (Focuses purely on ideation, hook, and technical clarity)
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an elite Tech Content Creator. Write high-engagement technical posts with a compelling hook, bullet takeaways, and call-to-action. Avoid corporate buzzwords."),
    ("human", "{prompt_text}")
])

# Agent 2: The Critic / Senior Editor (Rigorously evaluates against strict rubric)
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a ruthless Chief Content Editor. Evaluate on:
1. Hook & Engagement
2. Technical Substance
3. Readability & Formatting

Provide:
- SCORE: X/10
- 3 SPECIFIC ACTIONABLE CRITIQUES."""),
    ("human", "Topic: {topic}\n\nDraft:\n{draft}\n\nEvaluate thoroughly:")
])

writer_chain = writer_prompt | llm | StrOutputParser()
critic_chain = critic_prompt | llm | StrOutputParser()

# ── STEP 2: Score Extraction Utility ──
# Uses regex to extract numerical score out of 10 from critic's evaluation
def extract_score(review: str) -> float:
    match = re.search(r"SCORE:\s*(\d+(?:\.\d+)?)\s*/\s*10", review, re.I)
    return float(match.group(1)) if match else 7.0

# ── STEP 3: Multi-Agent Reflection & Quality Loop ──
def run_reflective_duo(topic: str, target_score: float = 8.0, max_rounds: int = 3):
    print("=" * 65)
    print(f"👥 MULTI-AGENT REFLECTION: WRITER & STRICT EDITOR DUO\n📌 TOPIC: \"{topic}\"\n🎯 TARGET SCORE: {target_score}/10")
    print("=" * 65)

    current_draft = ""
    last_feedback = ""

    # Loop until score target is met or max revision rounds reached
    for round_num in range(1, max_rounds + 1):
        print(f"\n✍️  [ROUND {round_num}/{max_rounds}] Creator Agent Writing...")
        if round_num == 1:
            prompt = f"Write an impactful technical post about: '{topic}'."
        else:
            # Pass editor's specific critiques back into the writer's context
            prompt = f"Revise the draft about '{topic}' by incorporating feedback:\n{last_feedback}\nPrevious:\n{current_draft}"

        current_draft = writer_chain.invoke({"prompt_text": prompt})
        print(f"🧐 [ROUND {round_num}/{max_rounds}] Editor Reviewing...")
        review = critic_chain.invoke({"topic": topic, "draft": current_draft})
        score = extract_score(review)
        print(f"📊 Score: {score}/10")

        # Convergence condition: approved if score meets target or rounds exhausted
        if score >= target_score or round_num == max_rounds:
            print(f"\n🎉 FINAL APPROVED DRAFT (Score: {score}/10 on Round {round_num})")
            with open("final_approved_post.md", "w") as f:
                f.write(current_draft)
            print("💾 Saved approved output to 'final_approved_post.md'\n")
            return current_draft

        # Save critique for next round's revision
        last_feedback = review
        print(f"🔄 Score {score} < {target_score}. Sending back for revision...")

if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "Why Agentic AI is the future of software development"
    run_reflective_duo(topic)
