# Day 1 - Session 1: Your First Local AI Chatbot
import sys
from langchain_ollama import ChatOllama

def main():
    print("🤖 Local AI Chatbot Initializing (Ollama + Llama 3.2)...")
    print("Type 'exit' or 'quit' to stop.\n" + "="*50)

    # Initialize local LLM via Ollama (Default: llama3.2)
    # Low-RAM laptops can use model="smollm:135m" or "tinyllama"
    try:
        llm = ChatOllama(model="llama3.2", temperature=0.7)
    except Exception as e:
        print(f"❌ Connection Error: Ensure Ollama is running (`ollama serve`). Details: {e}")
        sys.exit(1)

    while True:
        user_input = input("\n👤 You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        print("🤖 AI: ", end="", flush=True)
        try:
            # Stream tokens in real-time
            for chunk in llm.stream(user_input):
                print(chunk.content, end="", flush=True)
            print()
        except Exception as e:
            print(f"\n❌ Execution Error: {e}")

if __name__ == "__main__":
    main()
