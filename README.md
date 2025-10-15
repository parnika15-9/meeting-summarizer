Meeting Summarizer-
An AI-powered meeting transcription and summarization tool that converts audio recordings into actionable insights using Groq’s Whisper and Llama 3.3 models.
 
Features-

Audio Transcription: Converts meeting audio to text using Groq’s `whisper-large-v3-turbo`  
Smart Summarization: Generates concise summaries using Llama 3.3  
Action Items Extraction: Automatically identifies tasks and responsible parties  
Key Decisions Tracking: Highlights decisions made during meetings  
Multi-format Support: Accepts `MP3`, `WAV`, `M4A`, `MP4`, and `WebM` files  
History Management: View previous transcriptions and summaries  

Demo Video:

Tech Stack

Backend
- Python 3.10+
- Flask (REST API)
- Groq API (Whisper + Llama 3.3)
- Flask-CORS

Frontend
- HTML5  
- CSS3  
- Vanilla JavaScript 

Installation
1. Clone the repository
bashgit clone https://github.com/parnika15-9/meeting-summarizer.git
cd meeting-summarizer

3. Set up backend
bashcd backend
pip install -r requirements.txt

5. Configure environment variables
bash# Create .env file in backend folder

Windows Command Prompt:
copy .env.example .env

Linux/Mac:
cp .env.example .env

Edit .env and add your Groq API key:
GROQ_API_KEY=your_groq_api_key_here

4. Run the application

Start Backend:
bashcd backend
python app.py
Backend will run on http://127.0.0.1:5000

Open Frontend:
Simply open frontend/index.html in your browser
Or use a local server:
bashcd frontend
python -m http.server 8000
Then visit http://localhost:8000

Usage

Open the web interface in your browser
Click "Choose File" and select your meeting audio file
Click "Upload & Transcribe"
Wait for transcription and analysis (usually 30-60 seconds)
View Results:

Full transcript
Meeting summary
Key decisions
Action items
Discussion topics

Project Structure
meeting-summarizer/
├── backend/
│   ├── app.py              # Flask API server
│   ├── requirements.txt    # Python dependencies
│   └── .env.example       # Environment template
├── frontend/
│   ├── index.html         # Main UI
│   ├── style.css          # Styling
│   └── script.js          # Frontend logic
├── uploads/               # Temporary audio storage
├── transcripts/           # Saved transcriptions
├── demo/                  # Demo video
└── README.md             # Documentation

Key Features Breakdown
Transcription

Uses Groq's Whisper-large-v3-turbo model
Supports multiple audio formats
Fast processing (2-3x faster than real-time)

Summarization

Powered by Llama 3.3 70B
Structured JSON output
Extracts key information automatically

Future Enhancements

 Real-time transcription
 Speaker diarization (identify different speakers)
 Multi-language support
 Calendar integration
 Email summaries
 Team collaboration features
 Export to PDF/Word
