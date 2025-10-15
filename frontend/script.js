const API_URL = 'http://localhost:5000';

let selectedFile = null;

// DOM Elements
const uploadBox = document.getElementById('uploadBox');
const audioFile = document.getElementById('audioFile');
const uploadBtn = document.getElementById('uploadBtn');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const uploadSection = document.querySelector('.upload-section');

// Upload box click handler
uploadBox.addEventListener('click', () => {
    audioFile.click();
});

// File selection handler
audioFile.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleFileSelect(file);
    }
});

// Drag and drop handlers
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('drag-over');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('drag-over');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('drag-over');
    
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('audio/')) {
        handleFileSelect(file);
    } else {
        showError('Please drop an audio file');
    }
});

function handleFileSelect(file) {
    selectedFile = file;
    
    // Update UI
    const fileName = file.name.length > 30 ? file.name.substring(0, 30) + '...' : file.name;
    document.querySelector('.upload-text').textContent = `Selected: ${fileName}`;
    document.querySelector('.upload-subtext').textContent = `Size: ${(file.size / (1024 * 1024)).toFixed(2)} MB`;
    
    uploadBtn.disabled = false;
}

// Upload button handler
uploadBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    
    // Hide other sections
    uploadSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    loadingSection.style.display = 'block';
    
    try {
        // Create form data
        const formData = new FormData();
        formData.append('audio', selectedFile);
        
        // Update loading text
        document.getElementById('loadingText').textContent = 'Transcribing audio...';
        
        // Send to backend
        const response = await fetch(`${API_URL}/transcribe`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Upload failed');
        }
        
        document.getElementById('loadingText').textContent = 'Generating summary...';
        
        const result = await response.json();
        
        // Display results
        displayResults(result);
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    }
});

function displayResults(data) {
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'block';
    
    // Display transcript
    document.getElementById('transcript').textContent = data.transcript;
    
    // Display summary
    const analysis = data.analysis;
    document.getElementById('summary').textContent = analysis.summary || 'No summary available';
    
    // Display decisions
    const decisionsDiv = document.getElementById('decisions');
    if (Array.isArray(analysis.decisions) && analysis.decisions.length > 0) {
        decisionsDiv.innerHTML = '<ul>' + 
            analysis.decisions.map(d => `<li>${d}</li>`).join('') + 
            '</ul>';
    } else if (typeof analysis.decisions === 'string') {
        decisionsDiv.textContent = analysis.decisions;
    } else {
        decisionsDiv.textContent = 'No key decisions identified';
    }
    
    // Display action items
    const actionItemsDiv = document.getElementById('actionItems');
    if (Array.isArray(analysis.action_items) && analysis.action_items.length > 0) {
        actionItemsDiv.innerHTML = '<ul>' + 
            analysis.action_items.map(item => `<li>${item}</li>`).join('') + 
            '</ul>';
    } else if (typeof analysis.action_items === 'string') {
        actionItemsDiv.textContent = analysis.action_items;
    } else {
        actionItemsDiv.textContent = 'No action items identified';
    }
    
    // Display topics
    const topicsDiv = document.getElementById('topics');
    if (Array.isArray(analysis.topics) && analysis.topics.length > 0) {
        topicsDiv.innerHTML = '<ul>' + 
            analysis.topics.map(topic => `<li>${topic}</li>`).join('') + 
            '</ul>';
    } else if (typeof analysis.topics === 'string') {
        topicsDiv.textContent = analysis.topics;
    } else {
        topicsDiv.textContent = 'No topics identified';
    }
}

function showError(message) {
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'none';
    uploadSection.style.display = 'none';
    errorSection.style.display = 'block';
    
    document.getElementById('errorMessage').textContent = message;
}

// New meeting button
document.getElementById('newMeetingBtn').addEventListener('click', () => {
    resetApp();
});

// Retry button
document.getElementById('retryBtn').addEventListener('click', () => {
    resetApp();
});

function resetApp() {
    selectedFile = null;
    audioFile.value = '';
    document.querySelector('.upload-text').textContent = 'Click to upload or drag and drop';
    document.querySelector('.upload-subtext').textContent = 'MP3, WAV, M4A, WebM (Max 50MB)';
    uploadBtn.disabled = true;
    
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    uploadSection.style.display = 'block';
}

// Check server health on load
async function checkServerHealth() {
    try {
        const response = await fetch(`${API_URL}/health`);
        if (response.ok) {
            console.log('✅ Backend server is running');
        }
    } catch (error) {
        console.warn('⚠️ Backend server is not responding. Make sure to start it with: python backend/app.py');
    }
}

checkServerHealth();