# Quick Start Guide

## Fast Setup (Windows)

### Option 1: Automated Start

1. Double-click `start.bat` in the root folder
2. Wait for both servers to start
3. Open browser to http://localhost:5173

### Option 2: Manual Start

#### Terminal 1 - Backend:

```bash
cd backend
pip install -r requirements.txt
python main.py
```

#### Terminal 2 - Frontend:

```bash
cd RAG_
npm install
npm run dev
```

## First Time Setup

1. **Install Python 3.8+** (if not installed)
2. **Install Node.js 16+** (if not installed)
3. **Verify installations:**
   ```bash
   python --version
   node --version
   ```
4. Follow setup steps above

## Using the Application

1. **Upload a PDF**: Click "Choose PDF file" → Select file → Click "Upload"
2. **Ask Questions**: Type question → Press Enter or click Send
3. **View Answers**: See AI response with source citations
4. **Reset**: Click "Reset All" to clear everything

## Troubleshooting

### Backend won't start

- Check Python is installed: `python --version`
- Install dependencies: `cd backend && pip install -r requirements.txt`
- Verify .env file exists with OPENAI_API_KEY

### Frontend won't start

- Check Node.js is installed: `node --version`
- Install dependencies: `cd RAG_ && npm install`
- Try different port if 5173 is busy

### Can't connect

- Ensure both servers are running
- Backend should be on http://localhost:8000
- Frontend should be on http://localhost:5173

### Bad answers

- Upload clear, text-based PDFs (not scanned images)
- Make questions specific
- Try uploading more relevant documents

## Need Help?

See the full [README.md](README.md) for detailed documentation.
