# RAG Document Q&A System

A Retrieval-Augmented Generation (RAG) application that allows you to upload PDF documents and ask questions about their content. Uses free local embeddings and optionally OpenAI GPT for AI-generated answers.

## Features

- 📄 **Upload PDF Documents** — Process and index PDF files
- 💬 **Ask Questions** — Natural language queries about your documents
- 🎯 **Relevant Answers** — Context-aware responses with source citations
- 🔄 **Multiple Documents** — Upload and query across multiple documents
- 🧹 **Reset Database** — Clear all documents and start fresh
- 🎨 **Simple Interface** — Clean, intuitive chat-based UI
- 🆓 **Free Local Embeddings** — Uses HuggingFace `all-MiniLM-L6-v2` (no API key needed)
- 🔁 **LLM Fallback** — Works without OpenAI; returns relevant excerpts via similarity search

## Tech Stack

| Layer      | Technology                                      |
| ---------- | ----------------------------------------------- |
| Frontend   | React 19, TypeScript, Vite                      |
| Backend    | FastAPI, Uvicorn                                |
| Embeddings | HuggingFace Sentence Transformers (local, free) |
| Vector DB  | ChromaDB                                        |
| LLM        | OpenAI GPT-3.5-turbo (optional)                 |
| Framework  | LangChain                                       |

## Prerequisites

- Python 3.10+
- Node.js 20.19+ or 22.12+
- (Optional) OpenAI API key for AI-generated answers

## Installation

### 1. Clone the repository

```bash
cd "c:\Users\LENOVO\Rag model"
```

### 2. Backend Setup

#### Install Python dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### (Optional) Configure OpenAI for AI-generated answers

The app works without an API key (uses similarity search). For LLM-powered answers, create a `.env` file:

```bash
# backend/.env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Frontend Setup

#### Install Node dependencies

```bash
cd ../RAG_
npm install
```

## Running the Application

### 1. Start the Backend Server

Open a terminal and run:

```bash
cd backend
uvicorn main:app --reload --port 8000
```

The backend API will start at `http://localhost:8000`. Verify with `http://localhost:8000/health`.

> **Note:** The first run downloads the embedding model (~90 MB) — this is a one-time download.

### 2. Start the Frontend Development Server

Open a new terminal and run:

```bash
cd RAG_
npm run dev
```

The frontend will start at `http://localhost:5173` (or another port if 5173 is busy).

### 3. Access the Application

Open your browser and navigate to `http://localhost:5173`

## Usage Guide

### Uploading Documents

1. Click **"Choose PDF file"** to select a PDF document from your computer
2. Click the **"Upload"** button to process the document
3. Wait for the success confirmation
4. You can upload multiple documents - they will all be indexed together

### Asking Questions

1. Type your question in the input field at the bottom of the chat area
2. Press **Enter** or click the **Send** button
3. The AI will analyze your documents and provide a relevant answer
4. Source citations will be shown below the answer

### Resetting the Database

- Click the **"Reset All"** button to clear all uploaded documents and conversation history
- This action requires confirmation and cannot be undone

## API Endpoints

### Backend API

- `GET /` - API health check
- `GET /health` - Detailed health status
- `POST /upload` - Upload and process a PDF document
- `POST /ask` - Ask a question about uploaded documents
- `DELETE /reset` - Reset the vector database

## Project Structure

```
Rag model/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── Chunking.py          # Document processing utilities
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Environment variables
│   ├── uploaded_docs/       # Uploaded PDF files (auto-created)
│   └── chroma_db/          # Vector database storage (auto-created)
│
└── RAG_/
    ├── src/
    │   ├── App.tsx          # Main React component
    │   ├── App.css          # Application styles
    │   ├── main.tsx         # React entry point
    │   └── index.css        # Global styles
    ├── package.json         # Node dependencies
    └── vite.config.ts       # Vite configuration
```

## How It Works

1. **Document Upload**: PDFs are uploaded and split into chunks using LangChain's `RecursiveCharacterTextSplitter`
2. **Embedding**: Each chunk is converted into vector embeddings using the local HuggingFace `all-MiniLM-L6-v2` model (free, runs on CPU)
3. **Storage**: Embeddings are stored in ChromaDB for efficient similarity search
4. **Query**: When you ask a question, it's converted to an embedding using the same model
5. **Retrieval**: The most relevant document chunks are retrieved from ChromaDB
6. **Generation**: If an OpenAI API key is available, GPT-3.5-turbo generates a natural language answer from the retrieved context. Otherwise, the relevant excerpts are returned directly.
7. **Response**: The answer is returned with source document and page citations

## Troubleshooting

### Backend Issues

**"OPENAI_API_KEY not found"**

- This is just a warning — the app works without it using similarity search
- To enable LLM answers, add a `.env` file with your key in the `backend` folder

**OpenAI 429 quota error**

- The app automatically falls back to similarity search when OpenAI quota is exhausted
- Answers will be direct document excerpts instead of LLM-generated

**"Module not found"**

- Run `pip install -r requirements.txt` in the backend folder

### Frontend Issues

**"Cannot connect to backend"**

- Ensure the backend server is running on port 8000
- Check that both servers are running simultaneously

**"npm install fails"**

- Try deleting `node_modules` and `package-lock.json`, then run `npm install` again

### General Issues

**Slow responses**

- Large PDFs take time to process
- First startup downloads the embedding model (~90 MB)
- If OpenAI key is present but quota exhausted, there may be a brief delay before fallback kicks in

**Poor answer quality**

- Make sure documents are text-based PDFs (not scanned images)
- Try rephrasing your question
- Ensure relevant documents are uploaded

## Configuration

### Adjusting RAG Parameters

In [backend/main.py](backend/main.py), you can modify:

- `chunk_size`: Size of text chunks (default: 1000)
- `chunk_overlap`: Overlap between chunks (default: 200)
- `k`: Number of documents to retrieve (default: 3)
- `temperature`: Model creativity (default: 0.3, lower = more focused)
- `model_name`: OpenAI model to use (default: gpt-3.5-turbo)

### Changing the Model

To use GPT-4 instead of GPT-3.5-turbo:

```python
llm = ChatOpenAI(
    model_name="gpt-4",  # Change this
    temperature=0.3,
    openai_api_key=OPENAI_API_KEY
)
```

## Security Notes

- Keep your `.env` file private and never commit it to version control
- The `.env.example` file is provided as a template
- API keys in the code should be replaced with your own

## Future Enhancements

- Support for more document types (Word, TXT, etc.)
- Document management (view, delete individual documents)
- Conversation history persistence
- Multi-language support
- Advanced search filters
- Export conversation history

## License

MIT License - Feel free to use and modify as needed

## Support

If you encounter any issues or have questions, please check:

- OpenAI API status
- Python and Node.js versions
- Error messages in both terminal windows

---

**Enjoy using your RAG Document Q&A System! 🚀**
