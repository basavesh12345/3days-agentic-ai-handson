# Day 2 - Session 2: Document Analysis Graph with LangGraph
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class DocumentState(TypedDict):
    document: str
    summary: str
    keywords: List[str]
    questions: str

llm = ChatOllama(model="llama3.2", temperature=0.2)

def summarize_node(state: DocumentState) -> dict:
    print("📝 Step 1: Summarizing document...")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Summarize the document in 2 concise sentences."),
        ("human", "{document}")
    ])
    chain = prompt | llm | StrOutputParser()
    return {"summary": chain.invoke({"document": state["document"]})}

def extract_keywords_node(state: DocumentState) -> dict:
    print("🔑 Step 2: Extracting keywords...")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract 5 key technical terms as a comma-separated list."),
        ("human", "{document}")
    ])
    chain = prompt | llm | StrOutputParser()
    raw = chain.invoke({"document": state["document"]})
    return {"keywords": [k.strip() for k in raw.split(",")]}

def generate_questions_node(state: DocumentState) -> dict:
    print("❓ Step 3: Generating study questions...")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Generate 2 short exam questions based on the summary:\n{summary}"),
        ("human", "{document}")
    ])
    chain = prompt | llm | StrOutputParser()
    return {"questions": chain.invoke({"summary": state["summary"], "document": state["document"]})}

def build_graph():
    builder = StateGraph(DocumentState)
    builder.add_node("summarize", summarize_node)
    builder.add_node("extract_keywords", extract_keywords_node)
    builder.add_node("generate_questions", generate_questions_node)

    builder.add_edge(START, "summarize")
    builder.add_edge("summarize", "extract_keywords")
    builder.add_edge("extract_keywords", "generate_questions")
    builder.add_edge("generate_questions", END)

    return builder.compile()

if __name__ == "__main__":
    graph = build_graph()
    sample = "Agentic AI refers to systems where artificial intelligence models act as autonomous agents that reason, plan, and invoke tools."
    result = graph.invoke({"document": sample, "summary": "", "keywords": [], "questions": ""})
    print("\n📊 FINAL GRAPH RESULT:")
    print(f"Summary: {result['summary']}")
    print(f"Keywords: {result['keywords']}")
    print(f"Questions:\n{result['questions']}")
