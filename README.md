Meeting Summarizer

AI-powered meeting transcription and summarization tool that converts audio recordings into actionable insights using Groq's Whisper and Llama models.

 Features

- Audio Transcription: Converts meeting audio to text using Groq's Whisper-large-v3-turbo
- Smart Summarization: Generates concise meeting summaries using Llama 3.3
- Action Items Extraction: Automatically identifies tasks and responsible parties
- Key Decisions Tracking: Highlights important decisions made during meetings
- Multi-format Support: Supports MP3, WAV, M4A, MP4, and WebM files
- History Management: View past meeting transcriptions and summaries

 Demo Video:
 https://drive.google.com/file/d/1RSEmPb2a_Dw9XMz80WnYGhiyQ34bHkhf/view?usp=sharing

 Tech Stack

Backend:
- Python 3.10+
- Flask (REST API)
- Groq API (Whisper + Llama 3.3)
- Flask-CORS

Frontend:
- HTML5
- CSS3
- Vanilla JavaScript

 Prerequisites

- Python 3.10 or higher
- Groq API Key (Get one [here](https://console.groq.com/keys))
- Git

 Installation

 1. Clone the repository
```bash
git clone https://github.com/parnika15-9/meeting-summarizer.git
cd meeting-summarizer
```

 2. Set up backend
```bash
cd backend
pip install -r requirements.txt
```

 3. Configure environment variables
```bash
# Create .env file in backend folder
# Windows Command Prompt:
copy .env.example .env

# Linux/Mac:
cp .env.example .env

# Edit .env and add your Groq API key:
# GROQ_API_KEY=your_groq_api_key_here
```

 4. Run the application

**Start Backend:**
```bash
cd backend
python app.py
```

Backend will run on http://127.0.0.1:5000

**Open Frontend:** Simply open `frontend/index.html` in your browser

Or use a local server:
```bash
cd frontend
python -m http.server 8000
```

Then visit http://localhost:8000

 Usage

1. Open the web interface in your browser
2. Click "Choose File" and select your meeting audio file
3. Click "Upload & Transcribe"
4. Wait for transcription and analysis (usually 30-60 seconds)
5. View Results:
   - Full transcript
   - Meeting summary
   - Key decisions
   - Action items
   - Discussion topics

 Project Structure
```
meeting-summarizer/
├── backend/
│   ├── app.py              # Flask API server
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables (create this)
├── frontend/
│   ├── index.html         # Main UI
│   ├── style.css          # Styling
│   └── script.js          # Frontend logic
├── uploads/               # Temporary audio storage
├── transcripts/           # Saved transcriptions
└── README.md             # Documentation
```

 API Endpoints

 GET /

Health check and API information
```json
{
  "status": "running",
  "message": "Meeting Summarizer API is active!",
  "endpoints": {...}
}
```

 POST /transcribe

Upload audio file for transcription

- Body: multipart/form-data with audio file
- Returns: Transcript, summary, decisions, action items
```json
{
  "success": true,
  "transcript": "...",
  "analysis": {
    "summary": "...",
    "decisions": [...],
    "action_items": [...],
    "topics": [...]
  }
}
```

 GET /history

Retrieve last 10 transcription summaries

 GET /health

Server health status

 Key Features Breakdown

 Transcription
- Uses Groq's Whisper-large-v3-turbo model
- Supports multiple audio formats
- Fast processing (2-3x faster than real-time)

 Summarization
- Powered by Llama 3.3 70B
- Structured JSON output
- Extracts key information automatically

 Security Notes

- Never commit .env file with real API keys
- Use .env.example for templates
- Keep your Groq API key confidential
- Add .env to .gitignore

 Performance

- Transcription Speed: ~2-3x faster than real-time
- Summary Generation: 3-5 seconds
- Supported File Size: Up to 50MB
- Supported Formats: MP3, WAV, M4A, MP4, WebM

 Future Enhancements

- [ ] Real-time transcription
- [ ] Speaker diarization (identify different speakers)
- [ ] Multi-language support
- [ ] Calendar integration
- [ ] Email summaries
- [ ] Team collaboration features
- [ ] Export to PDF/Word

 License

MIT License - feel free to use for personal or commercial projects

 
 Author

Parnika
- GitHub: [@parnika15-9](https://github.com/parnika15-9)

 Acknowledgments

- Groq for providing fast AI inference
- OpenAI for Whisper model architecture
- Meta for Llama model

