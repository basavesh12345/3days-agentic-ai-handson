# Day 1 - Session 3: College Question Answering System (RAG)
import os
import sys
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# ── Configuration ──
MODEL = "llama3.2"
EMBED_MODEL = "nomic-embed-text"
CHROMA_PATH = "./chroma_db"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

def load_documents(file_path: str):
    """Load PDF or text file"""
    print(f"📄 Loading document: {file_path}")
    
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)
    
    docs = loader.load()
    print(f"✅ Loaded {len(docs)} page(s)")
    return docs

def split_documents(docs):
    """Split documents into smaller chunks"""
    print("✂️  Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_documents(docs)
    print(f"✅ Created {len(chunks)} chunks")
    return chunks

def create_vector_db(chunks):
    """Create and persist ChromaDB vector store"""
    print("🔢 Creating embeddings and storing in ChromaDB...")
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    print("✅ Vector database created!")
    return vectordb

def load_vector_db():
    """Load existing ChromaDB"""
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

def build_rag_chain(vectordb):
    """Build the RAG question-answering chain"""
    llm = ChatOllama(model=MODEL, temperature=0)
    retriever = vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}  # retrieve top 3 chunks
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant for answering questions 
        about college documents. Use ONLY the provided context to answer.
        If the answer is not in the context, say "I don't have that information 
        in the provided documents."
        
        Always mention which part of the document your answer comes from."""),
        ("human", """Context from documents:
        {context}
        
        Question: {question}
        
        Answer (with source reference):""")
    ])
    
    def format_docs(docs):
        return "\n\n".join([
            f"[Source: Page {doc.metadata.get('page', 'N/A')}]\n{doc.page_content}"
            for doc in docs
        ])
    
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

def main():
    print("🏫 College Q&A System (RAG)")
    print("=" * 45)
    
    # Check if DB exists, else create it
    if not os.path.exists(CHROMA_PATH):
        try:
            pdf_path = input("Enter path to your PDF/TXT file: ").strip()
        except EOFError:
            pdf_path = "college_info.txt"

        if not pdf_path or not os.path.exists(pdf_path):
            print("File not found! Creating demo with sample text...")
            # Create sample text file for demo
            with open("college_info.txt", "w") as f:
                f.write("""
Jyothy Institute of Technology - College Handbook

EXAMINATION RULES:
Students must carry their hall ticket to all examinations.
Mobile phones are strictly prohibited in examination halls.
Minimum 75% attendance is required to appear for exams.
Students found cheating will be expelled from the examination.

ATTENDANCE POLICY:
Regular attendance is mandatory for all students.
Students with less than 75% attendance will be detained.
Medical leave requires a medical certificate from a registered doctor.
Prior permission must be obtained for planned absences.

FEE STRUCTURE:
Tuition fee: Rs. 80,000 per year
Hostel fee: Rs. 60,000 per year (including meals)
Lab fee: Rs. 5,000 per semester
Bus facility available for selected routes.

LIBRARY RULES:
Library hours: 8:00 AM to 8:00 PM on working days
Students can borrow up to 3 books at a time
Books must be returned within 14 days
Late fee: Rs. 2 per day per book

PLACEMENT CELL:
The Placement Cell coordinates campus recruitment.
Students with CGPA above 6.0 are eligible for placement.
Mock interviews and aptitude training provided.
Companies visiting include TCS, Infosys, Wipro, Accenture.
                """)
            pdf_path = "college_info.txt"
        
        docs = load_documents(pdf_path)
        chunks = split_documents(docs)
        vectordb = create_vector_db(chunks)
    else:
        print("📂 Loading existing database...")
        vectordb = load_vector_db()
    
    chain = build_rag_chain(vectordb)
    
    print("\n🎉 Ready! Ask questions about the college documents.")
    print("Type 'quit' to exit.\n")
    
    while True:
        try:
            question = input("❓ Your question: ").strip()
        except EOFError:
            question = "What is the attendance requirement for exams?"
            print(f"❓ Your question: {question}")
            print("\n🤖 Answer:")
            answer = chain.invoke(question)
            print(answer)
            break

        if question.lower() in ['quit', 'exit']:
            break
        if not question:
            continue
        
        print("\n🤖 Answer:")
        answer = chain.invoke(question)
        print(answer)
        print("\n" + "-" * 45 + "\n")

if __name__ == "__main__":
    main()
