# =====================================================================
# Day 2 - Program 3: The Self-Healing Python Coder Agent
# Concept: Self-Correction Loop via Subprocess Execution & Error Feedback
# =====================================================================

# 1. Suppress internal deprecation warnings
import warnings
warnings.filterwarnings("ignore")

import re, sys, subprocess
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Low temperature (0.2) ensures code precision and fewer syntax mistakes
llm = ChatOllama(model="llama3.2", temperature=0.2)

# ── STEP 1: Code Block Extraction Utility ──
# Uses regex to isolate raw python code from any surrounding conversational prose
def extract_python_code(llm_output: str) -> str:
    match = re.search(r"```python\s*(.*?)\s*```", llm_output, re.DOTALL)
    return match.group(1).strip() if match else llm_output.strip()

# ── STEP 2: Secure Local Code Runner ──
# Runs the generated script in an isolated subprocess with a 10s timeout to catch infinite loops
def execute_code(code: str) -> tuple[bool, str]:
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True, text=True, timeout=10
        )
        # Exit code 0 means clean execution without exceptions
        if proc.returncode == 0:
            return True, proc.stdout.strip()
        else:
            # Return stderr containing the exact Python traceback
            return False, proc.stderr.strip()
    except Exception as e:
        return False, str(e)

# ── STEP 3: Self-Healing Agentic Loop ──
def self_healing_coder(user_task: str, max_attempts: int = 3):
    print("=" * 60)
    print(f"🎯 TASK: {user_task}")
    print("=" * 60)

    # Chain 1: Initial Code Generator
    coder_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert Python Engineer. Write clean, executable code wrapped inside ```python ... ``` blocks. Include print() statements."),
        ("human", "Task: {task}")
    ])

    # Chain 2: Bug Fixer & Error Healer (receives broken code + compiler error)
    fixer_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a senior debugging specialist. The previous code produced an error. Analyze the error traceback and return ONLY the complete fixed code inside ```python ... ```."),
        ("human", "Previous Code:\n```python\n{code}\n```\n\nExecution Error Traceback:\n{error}\n\nProvide corrected code:")
    ])

    coder_chain = coder_prompt | llm | StrOutputParser()
    fixer_chain = fixer_prompt | llm | StrOutputParser()

    current_code = ""
    last_error = ""

    # Iterative reflection cycle
    for attempt in range(1, max_attempts + 1):
        print(f"\n🔄 [Attempt {attempt}/{max_attempts}] Generating code...")
        if attempt == 1:
            raw = coder_chain.invoke({"task": user_task})
        else:
            # Pass the broken code and error traceback back into the model to self-correct
            raw = fixer_chain.invoke({"code": current_code, "error": last_error})

        current_code = extract_python_code(raw)
        print("💻 Executing code in subprocess...")
        success, output = execute_code(current_code)

        if success:
            print(f"\n🎉 CODE EXECUTED SUCCESSFULLY ON ATTEMPT {attempt}")
            print("=" * 60)
            print(current_code)
            print("-" * 60)
            print(f"📤 Output:\n{output}")
            print("=" * 60)
            return True
        else:
            # Capture error for the next healing attempt
            print(f"❌ Execution Failed on attempt {attempt}! Error:\n{output}")
            last_error = output

    return False

if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else "Calculate the sum of squares of even numbers between 1 and 10, format as a JSON string with key 'sum_of_even_squares', and print it."
    self_healing_coder(task)
