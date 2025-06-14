# Document Chatbot

An AI-powered chatbot system that allows users to upload documents (PDFs or images), query them for specific information, and generate thematic summaries — all through a user-friendly web interface. This project uses OCR, semantic search, and an open-source LLM for analysis.

---

## Project Structure
document-chatbot/
│
├── backend/ # FastAPI-based backend
│ ├── main.py # FastAPI app entry point
│ ├── routers/
│ │ ├── upload.py # Endpoint for document upload and text extraction
│ │ ├── query.py # Endpoint for answering queries based on uploaded content
│ │ └── theme.py # Endpoint for summarizing document themes
│ ├── services/
│ │ ├── ocr_service.py # OCR and text chunking logic
│ │ ├── vector_store.py # Embedding, ChromaDB storage, and semantic search
│ │ └── theme.py # LLM-based theme summarizer (Hugging Face model)
│ └── chroma_db/ # Persistent vector store (auto-created)
│
├── frontend/ # React-based frontend
│ ├── src/
│ │ ├── App.js # Main React layout with components
│ │ └── components/
│ │ ├── FileUploader.js # Handles file upload
│ │ ├── QueryBox.js # Lets user ask questions
│ │ └── ThemeViewer.js # Displays summarized themes
│ └── public/ # Static files and assets
│
├── requirements.txt # Python backend dependencies
└── README.md # This file



---

## LLM & Tech Stack

### Semantic Search
- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Used for**: Converting document chunks and queries into embeddings.

### Text Summarization (Theme Extraction)
- **Model**: `facebook/bart-large-cnn` (via Hugging Face Transformers)
- **Hosted via**: Hugging Face `pipeline("summarization")`
- **Open Source**: Yes
- **API-Free**: No OpenAI keys required.

---

##  Backend: FastAPI Endpoints

### 1. `/upload/` [POST]
Uploads a document (PDF, JPG, PNG, etc.), extracts its text (using OCR if needed), chunks it, and stores it into a vector database (ChromaDB).

**Request**:
- `file`: Form-data upload field

**Response**:
```json
{
  "status": "uploaded",
  "chunks": 18
}
```
### 2. `/query/` [POST]
Accepts a user query, searches the embedded chunks using vector similarity, and returns relevant matches.

**Request**:
- GET /query?q=What is Artificial Intelligence?

**Response**:
```json
{
  "question": "What is Artificial Intelligence?",
  "answers": [
    {
      "content": "AI refers to the simulation of human intelligence...",
      "meta": {
        "source": "uploaded_document.pdf"
      }
    }
  ]
}

```

### 3. `/theme/` [POST]
Accepts a user query, searches the embedded chunks using vector similarity, and returns relevant matches.

**Request**:
- GET /theme?q=Tell me about AI applications.
**Response**:
```json
{
    "question": "Tell me about AI applications",
    "themes": "Artificial Intelligence (AI) and Machine Learning (ML) are rapidly transforming industries. These technologies enable machines to learn from data and make intelligent decisions.\nArtificial Intelligence (AI) and Machine Learning (ML) are rapidly transforming industries. These technologies enable machines to learn from data and make"
}

```
## 🖥️ Frontend: React Components

### `App.js`
- Sets background and layout for the chatbot UI.

### `components/FileUploader.js`
- Uploads documents to the `/upload/` endpoint.
- Displays number of chunks extracted or error messages.

### `components/QueryBox.js`
- Allows user to type questions.
- Sends the query to `/query` endpoint.
- Displays the answers retrieved from the relevant document content.

### `components/ThemeViewer.js`
- Sends a summarization request to `/theme`.
- Displays document theme summary or error messages.

---

## Setup & Run

### Backend (Python + FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend (React + Tailwind CSS)

```bash
cd frontend
npm install
npm start
```


### 📦 Dependencies

# Backend
fastapi

uvicorn

transformers

sentence-transformers

chromadb

PyPDF2

pdf2image

pytesseract

Pillow

# Frontend
react

axios

tailwindcss
