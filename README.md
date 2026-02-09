# RAG Document Q&A System

A Retrieval-Augmented Generation (RAG) application that allows you to upload PDF documents and ask questions about their content. The system uses OpenAI's GPT models to provide accurate, context-aware answers based on your documents.

## Features

- 📄 **Upload PDF Documents** - Support for PDF file uploads
- 💬 **Ask Questions** - Natural language queries about your documents
- 🎯 **Relevant Answers** - AI-powered responses with source citations
- 🔄 **Multiple Documents** - Upload and query across multiple documents
- 🧹 **Reset Database** - Clear all documents and start fresh
- 🎨 **Simple Interface** - Clean, intuitive user interface

## Tech Stack

### Backend

- **FastAPI** - Modern Python web framework
- **LangChain** - LLM orchestration framework
- **OpenAI** - GPT-3.5-turbo for question answering
- **ChromaDB** - Vector database for document embeddings
- **PyPDF** - PDF document processing

### Frontend

- **React** - UI framework
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool
- **Lucide React** - Icon library

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- OpenAI API key

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

#### Configure environment variables

The `.env` file is already configured with your OpenAI API key. If you need to update it:

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
python main.py
```

The backend API will start at `http://localhost:8000`

You can verify it's running by visiting `http://localhost:8000/health`

### 2. Start the Frontend Development Server

Open a new terminal and run:

```bash
cd RAG_
npm run dev
```

The frontend will start at `http://localhost:5173` (or another port if 5173 is busy)

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

1. **Document Upload**: PDFs are uploaded and split into chunks using LangChain's text splitter
2. **Embedding**: Each chunk is converted into vector embeddings using OpenAI's embedding model
3. **Storage**: Embeddings are stored in ChromaDB for efficient retrieval
4. **Query**: When you ask a question, it's converted to an embedding
5. **Retrieval**: The most relevant document chunks are retrieved from ChromaDB
6. **Generation**: OpenAI's GPT-3.5-turbo generates an answer based on the retrieved context
7. **Response**: The answer is returned with source citations

## Troubleshooting

### Backend Issues

**"OPENAI_API_KEY not found"**

- Make sure the `.env` file exists in the `backend` folder
- Verify the API key is correctly set

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
- First query after upload may be slower as the model initializes

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
