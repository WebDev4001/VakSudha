class GestureDetector {
    constructor() {
        this.camera = null;
        this.videoElement = document.getElementById('camera-feed');
        this.canvasElement = document.getElementById('gesture-canvas');
        this.canvasCtx = this.canvasElement.getContext('2d');
        this.hands = null;
        this.isDetecting = false;
    }

    async initialize() {
        try {
            // Initialize MediaPipe Hands
            this.hands = new Hands({
                locateFile: (file) => {
                    return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
                }
            });

            this.hands.setOptions({
                maxNumHands: 2,
                modelComplexity: 1,
                minDetectionConfidence: 0.5,
                minTrackingConfidence: 0.5
            });

            this.hands.onResults((results) => this.onResults(results));

            // Setup camera
            const constraints = {
                video: {
                    width: 640,
                    height: 480,
                    facingMode: 'user'
                }
            };

            this.camera = await navigator.mediaDevices.getUserMedia(constraints);
            this.videoElement.srcObject = this.camera;
            this.videoElement.play();

            this.startDetection();
        } catch (error) {
            console.error('Error initializing gesture detection:', error);
            this.showError('Failed to initialize camera. Please check permissions.');
        }
    }

    async startDetection() {
        if (this.isDetecting) return;
        
        this.isDetecting = true;
        await this.hands.send({image: this.videoElement});
        this.detect();
    }

    async detect() {
        if (!this.isDetecting) return;

        await this.hands.send({image: this.videoElement});
        requestAnimationFrame(() => this.detect());
    }

    stopDetection() {
        this.isDetecting = false;
        if (this.camera) {
            const tracks = this.camera.getTracks();
            tracks.forEach(track => track.stop());
        }
    }

    onResults(results) {
        // Clear canvas
        this.canvasCtx.clearRect(0, 0, this.canvasElement.width, this.canvasElement.height);
        this.canvasCtx.drawImage(results.image, 0, 0, this.canvasElement.width, this.canvasElement.height);

        if (results.multiHandLandmarks) {
            for (const landmarks of results.multiHandLandmarks) {
                drawConnectors(this.canvasCtx, landmarks, HAND_CONNECTIONS, {
                    color: '#00FF00',
                    lineWidth: 5
                });
                drawLandmarks(this.canvasCtx, landmarks, {
                    color: '#FF0000',
                    lineWidth: 2
                });
            }

            this.analyzeGesture(results.multiHandLandmarks);
        }
    }

    analyzeGesture(landmarks) {
        // Implement basic gesture recognition
        // This is a simplified version - you can expand based on needs
        if (landmarks.length > 0) {
            const hand = landmarks[0];
            
            // Check if fingers are extended
            const fingersExtended = this.checkFingersExtended(hand);
            
            // Update the gesture feedback
            document.getElementById('gesture-feedback').textContent = 
                `Detected fingers: ${fingersExtended.join(', ')}`;
        }
    }

    checkFingersExtended(hand) {
        const fingers = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky'];
        const extended = [];

        // Simplified finger detection
        // You can make this more sophisticated based on your needs
        const fingerTips = [4, 8, 12, 16, 20];
        const fingerBases = [2, 5, 9, 13, 17];

        fingerTips.forEach((tip, index) => {
            if (hand[tip].y < hand[fingerBases[index]].y) {
                extended.push(fingers[index]);
            }
        });

        return extended;
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
