class SpeechAnalyzer {
    constructor() {
        this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        this.recognition.continuous = false;
        this.recognition.interimResults = true;
        this.isRecording = false;
        this.setupRecognition();
    }

    setupRecognition() {
        this.recognition.onresult = (event) => {
            const transcript = Array.from(event.results)
                .map(result => result[0])
                .map(result => result.transcript)
                .join('');

            if (event.results[0].isFinal) {
                this.analyzeSpeech(transcript);
            }
            
            // Update the live transcript
            document.getElementById('live-transcript').textContent = transcript;
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.stopRecording();
            this.showError('Speech recognition failed. Please try again.');
        };
    }

    startRecording() {
        if (this.isRecording) return;
        
        try {
            this.recognition.start();
            this.isRecording = true;
            document.getElementById('record-btn').classList.add('recording');
            document.getElementById('record-status').textContent = 'Recording...';
        } catch (error) {
            console.error('Failed to start recording:', error);
            this.showError('Failed to start recording. Please try again.');
        }
    }

    stopRecording() {
        if (!this.isRecording) return;
        
        this.recognition.stop();
        this.isRecording = false;
        document.getElementById('record-btn').classList.remove('recording');
        document.getElementById('record-status').textContent = 'Click to start recording';
    }

    async analyzeSpeech(transcript) {
        try {
            const response = await fetch('/api/analyze-speech', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: transcript })
            });

            if (!response.ok) {
                throw new Error('Speech analysis failed');
            }

            const analysis = await response.json();
            this.displayResults(analysis);
        } catch (error) {
            console.error('Analysis error:', error);
            this.showError('Failed to analyze speech. Please try again.');
        }
    }

    displayResults(analysis) {
        const resultsDiv = document.getElementById('analysis-results');
        resultsDiv.innerHTML = `
            <div class="card mt-3">
                <div class="card-body">
                    <h5 class="card-title">Analysis Results</h5>
                    <p>Score: ${analysis.score}/10</p>
                    <p>Feedback: ${analysis.feedback}</p>
                    <h6>Suggested Improvements:</h6>
                    <ul>
                        ${analysis.improvements.map(imp => `<li>${imp}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `;
    }

    showError(message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger alert-dismissible fade show';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.getElementById('alerts').appendChild(alertDiv);
    }
}
