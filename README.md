# AI Project Intelligence Assistant

A RAG-based system for document Q&A and data analysis.

## Tech Stack

- **Backend**: Python, FastAPI, LangChain
- **Frontend**: React (JavaScript)
- **Vector DB**: Chroma (local)
- **Data Processing**: Pandas
- **LLM**: Google Gemini API

## Features

- Upload PDF, CSV, Excel files
- RAG-powered document Q&A with source citations
- Data analysis with natural language explanations
- Multi-agent routing system
- Conversation memory
- Real-time chat interface

## Quick Start

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Backend runs on `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000`

### Generate Sample Data

```bash
cd sample_data
pip install -r requirements.txt
python generate_samples.py
```

## Project Structure

```
backend/
├── agents/              # Router, Document Q&A, Data Analysis agents
├── routes/              # FastAPI endpoints (upload, query)
├── services/            # RAG pipeline, vector store, data analyzer
├── utils/               # File handling, text chunking
├── config.py            # Settings and configuration
└── main.py              # FastAPI application

frontend/
├── src/
│   ├── components/      # FileUpload, ChatInterface, Message
│   ├── App.js           # Main application
│   └── index.js         # Entry point
└── package.json

sample_data/             # Synthetic datasets for testing
```

## API Endpoints

- `POST /api/upload` - Upload files
- `POST /api/query` - Ask questions
- `GET /api/files` - List uploaded files
- `GET /api/history/{session_id}` - Get conversation history

## Deployment

### 1. Render
### 2. Railway

## Environment Variables

```
GOOGLE_API_KEY=your_google_api_key_here
CHROMA_PERSIST_DIR=./chroma_db
UPLOAD_DIR=./uploads
```

**Get your Google API key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey) to create a free API key.

## Usage

1. Upload PDF or CSV/Excel files
2. Ask questions in the chat interface
3. System routes to appropriate agent
4. View answers with sources/analysis

## Example Questions

- "What is the project budget?"
- "Calculate the total expenses"
- "What are the main objectives?"
- "Are there any anomalies in the data?"
