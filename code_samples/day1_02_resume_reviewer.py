# Day 1 - Session 2: AI Resume Reviewer using LangChain LCEL
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def analyze_resume(resume_text: str, target_role: str):
    # 1. Initialize LLM
    llm = ChatOllama(model="llama3.2", temperature=0.2)

    # 2. Define Prompt Template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert HR Manager and Technical Recruiter.
Analyze the provided resume for the position of '{role}'.
Provide a structured evaluation with:
1. ATS Match Score (0 to 100)
2. Top 3 Strengths
3. Top 3 Weaknesses / Missing Keywords
4. Recommended Section Rewrites"""),
        ("human", "Resume Content:\n{resume}")
    ])

    # 3. Build LCEL Chain (Prompt -> LLM -> Parser)
    chain = prompt | llm | StrOutputParser()

    print(f"📄 Analyzing resume for target role: '{target_role}'...")
    print("=" * 55)

    # 4. Invoke Chain
    result = chain.invoke({"role": target_role, "resume": resume_text})
    print(result)

if __name__ == "__main__":
    sample_resume = """
    Jane Doe | Software Engineering Student
    Skills: Python, Java, Data Structures, HTML/CSS, SQL.
    Projects:
    - Built a Library Management System in Python using SQLite.
    - Weather app with JavaScript API.
    Education: B.E. in Computer Science (GPA: 8.5/10).
    """
    analyze_resume(sample_resume, target_role="AI / ML Software Engineer")
