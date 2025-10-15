from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
from dotenv import load_dotenv
from pathlib import Path
import json
from datetime import datetime

# Load environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
print(f"Loading .env from: {env_path.absolute()}")
print(f"API Key found: {os.getenv('GROQ_API_KEY') is not None}")

app = Flask(__name__)
CORS(app)

# Configure Groq Client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Create necessary directories
UPLOAD_FOLDER = Path('../uploads')
TRANSCRIPT_FOLDER = Path('../transcripts')
UPLOAD_FOLDER.mkdir(exist_ok=True)
TRANSCRIPT_FOLDER.mkdir(exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'status': 'running',
        'message': 'Meeting Summarizer API is active! (Powered by Groq)',
        'endpoints': {
            'health': '/health (GET) - Check server health',
            'transcribe': '/transcribe (POST) - Upload audio file for transcription',
            'history': '/history (GET) - Get transcription history'
        },
        'usage': {
            'transcribe': 'Send POST request with audio file in form-data with key "audio"',
            'supported_formats': list(ALLOWED_EXTENSIONS)
        }
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Server is running with Groq API'}), 200

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        # Check if file is present
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: mp3, mp4, wav, m4a, webm'}), 400
        
        # Save file temporarily
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{file.filename}"
        filepath = app.config['UPLOAD_FOLDER'] / filename
        file.save(filepath)
        
        # Transcribe using Groq Whisper
        print(f"Transcribing file: {filename}")
        with open(filepath, 'rb') as audio_file:
            transcript_response = client.audio.transcriptions.create(
                model="whisper-large-v3-turbo",
                file=audio_file,
                response_format="text"
            )
        
        # Groq returns the transcript directly as a string
        transcript_text = transcript_response
        
        # Generate summary and action items using Groq LLM
        print("Generating summary and action items...")
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert meeting assistant. Analyze meeting transcripts and provide structured summaries."
                },
                {
                    "role": "user",
                    "content": f"""Analyze this meeting transcript and provide:

1. **Meeting Summary**: A concise overview (3-5 sentences)
2. **Key Decisions**: List all important decisions made
3. **Action Items**: List all tasks with responsible parties if mentioned
4. **Key Topics Discussed**: Main discussion points

Transcript:
{transcript_text}

Format your response as JSON with keys: summary, decisions, action_items, topics"""
                }
            ],
            temperature=0.7
        )
        
        # Parse LLM response
        llm_response = completion.choices[0].message.content
        
        # Try to parse as JSON, fallback to structured text
        try:
            # Remove markdown code blocks if present
            if '```json' in llm_response:
                llm_response = llm_response.split('```json')[1].split('```')[0].strip()
            elif '```' in llm_response:
                llm_response = llm_response.split('```')[1].split('```')[0].strip()
            
            analysis = json.loads(llm_response)
        except:
            # Fallback parsing
            analysis = {
                "summary": "Could not parse structured response",
                "decisions": [],
                "action_items": [],
                "topics": [],
                "raw_response": llm_response
            }
        
        # Save transcript and analysis
        output_data = {
            'filename': filename,
            'timestamp': timestamp,
            'transcript': transcript_text,
            'analysis': analysis
        }
        
        output_file = TRANSCRIPT_FOLDER / f"{timestamp}_analysis.json"
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        # Clean up uploaded file (optional)
        # os.remove(filepath)
        
        return jsonify({
            'success': True,
            'transcript': transcript_text,
            'analysis': analysis,
            'saved_to': str(output_file)
        }), 200
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    try:
        files = list(TRANSCRIPT_FOLDER.glob('*.json'))
        history = []
        
        for file in sorted(files, reverse=True)[:10]:  # Last 10 files
            with open(file, 'r') as f:
                data = json.load(f)
                history.append({
                    'timestamp': data['timestamp'],
                    'filename': data['filename'],
                    'summary': data['analysis'].get('summary', 'No summary available')[:100]
                })
        
        return jsonify({'history': history}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Meeting Summarizer Backend...")
    print(f"Upload folder: {UPLOAD_FOLDER.absolute()}")
    print(f"Transcript folder: {TRANSCRIPT_FOLDER.absolute()}")
    app.run(debug=True, port=5000)