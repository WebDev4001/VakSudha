document.addEventListener('DOMContentLoaded', function() {
    // Initialize speech analyzer if on practice page
    if (document.getElementById('speech-practice')) {
        const speechAnalyzer = new SpeechAnalyzer();
        
        document.getElementById('record-btn').addEventListener('click', function() {
            if (speechAnalyzer.isRecording) {
                speechAnalyzer.stopRecording();
            } else {
                speechAnalyzer.startRecording();
            }
        });
    }

    // Initialize gesture detector if on gesture practice page
    if (document.getElementById('gesture-practice')) {
        const gestureDetector = new GestureDetector();
        
        document.getElementById('start-gesture').addEventListener('click', async function() {
            await gestureDetector.initialize();
            this.disabled = true;
            document.getElementById('stop-gesture').disabled = false;
        });

        document.getElementById('stop-gesture').addEventListener('click', function() {
            gestureDetector.stopDetection();
            this.disabled = true;
            document.getElementById('start-gesture').disabled = false;
        });
    }

    // Handle progress saving
    const saveProgress = async (exerciseId, score, feedback) => {
        try {
            const response = await fetch('/api/save-progress', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    exercise_id: exerciseId,
                    score: score,
                    feedback: feedback
                })
            });

            if (!response.ok) {
                throw new Error('Failed to save progress');
            }

            showAlert('Progress saved successfully!', 'success');
        } catch (error) {
            console.error('Error saving progress:', error);
            showAlert('Failed to save progress. Please try again.', 'danger');
        }
    };

    // Utility function for showing alerts
    const showAlert = (message, type) => {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.getElementById('alerts').appendChild(alertDiv);
    };

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
