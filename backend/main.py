from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

app = FastAPI(title="RAG API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
UPLOAD_DIR = Path("uploaded_docs")
UPLOAD_DIR.mkdir(exist_ok=True)
CHROMA_DIR = Path("chroma_db")
CHROMA_DIR.mkdir(exist_ok=True)

# Global variables for RAG components
vectorstore = None
qa_chain = None

# Initialize - FREE local embeddings (no API key needed)
print("Loading embedding model (first time may take a minute to download)...")
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)
print("Embedding model loaded!")

# OpenAI for chat (only used when asking questions)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
llm = None
if OPENAI_API_KEY:
    try:
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.3,
            openai_api_key=OPENAI_API_KEY,
            request_timeout=10,
            max_retries=0
        )
    except Exception as e:
        print(f"Warning: Could not initialize OpenAI LLM: {e}")


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    answer: str
    source_documents: Optional[List[str]] = []


def process_document(file_path: str):
    """Process uploaded document and add to vector store"""
    global vectorstore, qa_chain
    
    # Load PDF
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    
    # Create or update vector store
    if vectorstore is None:
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=str(CHROMA_DIR),
            collection_name="rag_documents"
        )
    else:
        vectorstore.add_documents(chunks)
    
    # Create QA chain with custom prompt
    prompt_template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Always provide a clear and concise answer based on the context.
    
    Context: {context}
    
    Question: {question}
    
    Answer:"""
    
    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    if llm is not None:
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": PROMPT}
        )


@app.get("/")
async def root():
    return {"message": "RAG API is running"}


@app.get("/health")
async def health_check():
    doc_count = 0
    if vectorstore:
        try:
            doc_count = len(vectorstore.get()['ids']) if vectorstore.get() else 0
        except:
            doc_count = "unknown"
    
    return {
        "status": "healthy",
        "vectorstore_initialized": vectorstore is not None,
        "documents_count": doc_count
    }


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        process_document(str(file_path))
        
        return {
            "message": "Document uploaded and processed successfully",
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question about uploaded documents"""
    try:
        if vectorstore is None:
            raise HTTPException(
                status_code=400,
                detail="No documents uploaded yet. Please upload a document first."
            )
        
        # Helper: fallback to similarity search (no LLM needed)
        def similarity_fallback(question: str):
            docs = vectorstore.similarity_search(question, k=3)
            if not docs:
                return QuestionResponse(
                    answer="No relevant information found in the uploaded documents.",
                    source_documents=[]
                )
            context = "\n\n".join([doc.page_content for doc in docs])
            sources = []
            for doc in docs:
                source_info = doc.metadata.get("source", "Unknown")
                page = doc.metadata.get("page", "N/A")
                sources.append(f"{Path(source_info).name} (Page {page + 1})")
            answer = f"Based on the documents, here is the relevant information:\n\n{context}"
            return QuestionResponse(
                answer=answer,
                source_documents=sources
            )

        # If OpenAI LLM is available, try the QA chain first
        if qa_chain is not None:
            try:
                result = qa_chain.invoke({"query": request.question})
                sources = []
                if "source_documents" in result:
                    for doc in result["source_documents"]:
                        source_info = doc.metadata.get("source", "Unknown")
                        page = doc.metadata.get("page", "N/A")
                        sources.append(f"{Path(source_info).name} (Page {page + 1})")
                return QuestionResponse(
                    answer=result["result"],
                    source_documents=sources
                )
            except Exception as llm_error:
                print(f"LLM failed ({llm_error}), falling back to similarity search")
                return similarity_fallback(request.question)
        else:
            # Fallback: use similarity search and return relevant chunks directly
            return similarity_fallback(request.question)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")


@app.delete("/reset")
async def reset_database():
    """Reset the vector database"""
    global vectorstore, qa_chain
    
    try:
        if vectorstore:
            vectorstore = None
        qa_chain = None
        
        if CHROMA_DIR.exists():
            shutil.rmtree(CHROMA_DIR)
            CHROMA_DIR.mkdir(exist_ok=True)
        
        if UPLOAD_DIR.exists():
            for file in UPLOAD_DIR.glob("*"):
                file.unlink()
        
        return {"message": "Database reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting database: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
