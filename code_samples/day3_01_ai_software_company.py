# Day 3 - Session 1: AI Software Company with CrewAI
import os
from crewai import Agent, Task, Crew, Process, LLM

# Configure Ollama LLM backend for CrewAI
local_llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
)

# ── 1. Define the Agents ──

project_manager = Agent(
    role="Project Manager",
    goal="Break down software requirements into clear tasks and coordinate the team",
    backstory="""You are an experienced software project manager with 10 years 
    of experience. You excel at understanding requirements and planning 
    structured development workflows. You're organized, clear, and pragmatic.""",
    llm=local_llm,
    verbose=True,
    allow_delegation=False
)

researcher = Agent(
    role="Senior Technical Researcher",
    goal="Research best approaches, algorithms, and design patterns for the given problem",
    backstory="""You are a senior software architect who loves exploring different 
    approaches to solve problems. You know multiple programming paradigms, 
    design patterns, and best practices. You provide thorough analysis.""",
    llm=local_llm,
    verbose=True,
    allow_delegation=False
)

developer = Agent(
    role="Senior Python Developer",
    goal="Write clean, efficient, well-commented Python code based on the research",
    backstory="""You are a senior Python developer with expertise in writing 
    production-quality code. You follow PEP 8 standards, add proper comments,
    handle edge cases, and write readable, maintainable code.""",
    llm=local_llm,
    verbose=True,
    allow_delegation=False
)

tester = Agent(
    role="QA Engineer",
    goal="Review the code, identify bugs, and write comprehensive test cases",
    backstory="""You are a meticulous QA engineer who thinks about edge cases,
    input validation, and failure scenarios. You write pytest test cases 
    and provide specific, actionable feedback on code quality.""",
    llm=local_llm,
    verbose=True,
    allow_delegation=False
)

doc_writer = Agent(
    role="Technical Documentation Writer",
    goal="Create clear, comprehensive documentation including README and usage examples",
    backstory="""You write excellent technical documentation that developers love.
    You include installation instructions, usage examples, API references,
    and troubleshooting tips. Your READMEs are always GitHub-ready.""",
    llm=local_llm,
    verbose=True,
    allow_delegation=False
)

# ── 2. Define the Tasks ──

def create_tasks(project_requirement: str):
    
    plan_task = Task(
        description=f"""Analyze this software requirement and create a structured plan:
        
        Requirement: {project_requirement}
        
        Create:
        1. Clear understanding of what needs to be built
        2. List of key features to implement
        3. Suggested data structures or classes needed
        4. Step-by-step implementation plan (5-7 steps)""",
        expected_output="A structured project plan with features, data structures, and implementation steps",
        agent=project_manager
    )
    
    research_task = Task(
        description="""Based on the project plan, research and recommend:
        1. Best Python libraries to use (if any)
        2. Most suitable data structures 
        3. Design patterns to apply
        4. Potential edge cases to handle
        5. Common pitfalls to avoid""",
        expected_output="Technical recommendations including libraries, patterns, and edge cases",
        agent=researcher,
        context=[plan_task]
    )
    
    code_task = Task(
        description="""Write complete, working Python code based on the plan and research.
        Requirements:
        - Full implementation with all features
        - Proper error handling and input validation
        - Clear variable names and comments
        - Example usage at the bottom
        - PEP 8 compliant""",
        expected_output="Complete, runnable Python code with comments and examples",
        agent=developer,
        context=[plan_task, research_task],
        output_file="solution.py"
    )
    
    test_task = Task(
        description="""Review the Python code and:
        1. Identify any bugs or logical errors
        2. Check edge case handling  
        3. Write 5 pytest test cases covering:
           - Normal usage (happy path)
           - Edge cases (empty input, large input)
           - Error cases (invalid input)
        4. Suggest any improvements""",
        expected_output="Code review feedback + 5 pytest test cases + improvement suggestions",
        agent=tester,
        context=[code_task],
        output_file="test_solution.py"
    )
    
    doc_task = Task(
        description="""Create a professional README.md for this project including:
        1. Project title and description
        2. Features list
        3. Installation instructions
        4. Usage examples with code snippets
        5. Function/class documentation
        6. Example output
        7. Contributing guidelines""",
        expected_output="Complete README.md in markdown format, ready for GitHub",
        agent=doc_writer,
        context=[code_task, test_task],
        output_file="README.md"
    )
    
    return [plan_task, research_task, code_task, test_task, doc_task]

# ── 3. Create and Run the Crew ──
def main():
    print("🏢 AI Software Company — CrewAI")
    print("=" * 50)
    print("Agents: Project Manager | Researcher | Developer | Tester | Doc Writer")
    print("=" * 50)
    
    requirement = input("\n📋 Enter your software requirement:\n> ").strip()
    
    if not requirement:
        requirement = (
            "Build a Python library for managing a student grade book that can "
            "add students, record grades, calculate GPA, and generate a report card"
        )
        print(f"\nUsing default: {requirement}")
    
    tasks = create_tasks(requirement)
    
    crew = Crew(
        agents=[project_manager, researcher, developer, tester, doc_writer],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    print("\n🚀 Crew is working... (this may take 2-4 minutes with local LLM)\n")
    result = crew.kickoff()
    
    print("\n" + "=" * 50)
    print("✅ CREW COMPLETED!")
    print("=" * 50)
    print("\n📄 Generated Deliverables:")
    print("  1. Code:        solution.py")
    print("  2. Test Suite:  test_solution.py")
    print("  3. Docs:        README.md")
    print("\n--- Final Documentation Preview ---")
    print(result.raw)

if __name__ == "__main__":
    main()
