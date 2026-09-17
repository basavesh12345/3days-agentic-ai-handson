# Day 1 - Session 3: College Question Answering System (RAG)
import os
import sys
import shutil
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

def create_sample_handbook():
    """Create sample college handbook text file if no PDF is provided"""
    file_path = "college_info.txt"
    with open(file_path, "w") as f:
        f.write("""Jyothy Institute of Technology - College Handbook

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
    return file_path

def load_documents(file_path: str):
    """Load PDF or text file automatically based on file extension"""
    print(f"📄 Loading document: {file_path}")
    
    # PyPDFLoader parses .pdf files page by page
    if file_path.lower().endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)
        
    docs = loader.load()
    print(f"✅ Loaded {len(docs)} page(s)")
    return docs

def split_documents(docs):
    """Split documents into smaller chunks"""
    print("✂️ Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_documents(docs)
    print(f"✅ Created {len(chunks)} chunks")
    return chunks

def build_vector_db(document_path: str):
    """Create and persist fresh ChromaDB vector store from given PDF/TXT file"""
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    docs = load_documents(document_path)
    chunks = split_documents(docs)

    print("🔢 Creating embeddings and storing in ChromaDB...")
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    print("✅ Vector database created!")
    return vectordb

def build_rag_chain(vectordb):
    """Build the RAG question-answering chain"""
    llm = ChatOllama(model=MODEL, temperature=0)
    retriever = vectordb.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant for answering questions 
about college documents. Use ONLY the provided context to answer.
If the answer is not in the context, say "I don't have that information in the provided documents."

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

    # 1. Determine Document Path (CLI Argument or fallback to demo)
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        file_path = sys.argv[1]
    else:
        file_path = create_sample_handbook()

    # 2. Build Vector DB & RAG Chain
    vectordb = build_vector_db(file_path)
    chain = build_rag_chain(vectordb)
    
    # 3. Ask Question
    question = "What is the attendance requirement for exams?"
    print(f"\n❓ Question: {question}")
    print("🤖 Answer:\n")
    print(chain.invoke(question))

if __name__ == "__main__":
    main()
