# InsightFlow - AI-based Q&A RAG System

InsightFlow is a web application that transcribes, summarizes, and enables Q&A over audio, video, documents, and links using advanced AI models. It leverages Retrieval-Augmented Generation (RAG) and vector search for accurate, context-aware answers.

## Features
- Transcribe audio and video files to text (AssemblyAI)
- Summarize meeting content using LLMs (Cohere, AI21)
- Q&A over meeting content using RAG
- Supports documents and web links
- Video-to-audio extraction
- Semantic search with FAISS vector database
- User authentication and secure file upload
- Automated email delivery of summaries
- AES-256 encryption for sensitive data
- Scalable deployment (Render, Vercel)

## Tech Stack
- **Frontend:** React.js
- **Backend:** FastAPI
- **Database:** MongoDB
- **Vector Search:** FAISS
- **AI/LLM APIs:** AssemblyAI, Cohere, AI21
- **Deployment:** Render (backend), Vercel (frontend)

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB instance
- AssemblyAI, Cohere, and AI21 API keys

### Backend (FastAPI)
1. Clone the repository:
   ```bash
   git clone https://github.com/Kprateek283/Insightflow.git
   cd Insightflow/backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your `.env` file with the required API keys and MongoDB URI.
5. Run the backend server:
   ```basho
   uvicorn main:app --reload
   ```

### Frontend (React.js)
1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Set up your environment variables (e.g., API base URL).
4. Run the frontend:
   ```bash
   npm start
   ```

## Usage
- Register or log in to your account.
- Upload audio, video, document, or link.
- Wait for transcription and summary generation.
- Ask questions about your content and receive context-aware answers.
- Download or receive summaries via email.

## Security
- All sensitive data is encrypted using AES-256.
- JWT-based authentication for secure access.

## Contribution
Contributions are welcome! Please open issues or submit pull requests for improvements or bug fixes.

## License
This project is licensed under the MIT License.

## Contact
For questions or support, contact [kprateek283@gmail.com](mailto:kprateek283@gmail.com).

---

**GitHub:** https://github.com/Kprateek283/Insightflow 