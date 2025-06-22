// Socket.IO Connection
const socket = io();

// DOM Elements
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const videoFeed = document.getElementById('videoFeed');
const videoPlaceholder = document.getElementById('videoPlaceholder');
const detectionOverlay = document.getElementById('detectionOverlay');
const connectionStatus = document.getElementById('connectionStatus');
const connectionText = document.getElementById('connectionText');
const detectionStatus = document.getElementById('detectionStatus');
const detectionText = document.getElementById('detectionText');
const faceCount = document.getElementById('faceCount');
const maskCount = document.getElementById('maskCount');
const noMaskCount = document.getElementById('noMaskCount');
// State Variables
let isDetecting = false;
let detectionStats = {
    faces: 0,
    withMask: 0,
    withoutMask: 0
};

function updateConnectionStatus(connected) {
    if (connected) {
        connectionStatus.className = 'fas fa-circle status-indicator connected';
        connectionText.textContent = 'Terhubung';
    } else {
        connectionStatus.className = 'fas fa-circle status-indicator disconnected';
        connectionText.textContent = 'Terputus';
    }
}

function updateDetectionStatus(detecting) {
    if (detecting) {
        detectionStatus.className = 'fas fa-video status-indicator detecting';
        detectionText.textContent = 'Mendeteksi...';
        startBtn.disabled = true;
        stopBtn.disabled = false;
        detectionOverlay.classList.add('active');
    } else {
        detectionStatus.className = 'fas fa-video status-indicator';
        detectionText.textContent = 'Siap untuk deteksi';
        startBtn.disabled = false;
        stopBtn.disabled = true;
        detectionOverlay.classList.remove('active');
        videoFeed.style.display = 'none';
        videoPlaceholder.style.display = 'flex';
    }
    isDetecting = detecting;
}

function updateDetectionStats(detections) {
    let faces = detections.length;
    let withMask = 0;
    let withoutMask = 0;
    
    detections.forEach(detection => {
        if (detection.label === 'Mask') {
            withMask++;
        } else {
            withoutMask++;
        }
    });
    
    detectionStats = { faces, withMask, withoutMask };
    
    faceCount.textContent = faces;
    maskCount.textContent = withMask;
    noMaskCount.textContent = withoutMask;
}



// Event Listeners
startBtn.addEventListener('click', () => {
    socket.emit('start_detection');
});

stopBtn.addEventListener('click', () => {
    socket.emit('stop_detection');
});

// Socket Event Handlers
socket.on('connect', () => {
    updateConnectionStatus(true);
});

socket.on('disconnect', () => {
    updateConnectionStatus(false);
    updateDetectionStatus(false);
});

socket.on('connection_status', (data) => {
    // Connection status handled by connect/disconnect events
});

socket.on('detection_status', (data) => {
    if (data.status === 'started') {
        updateDetectionStatus(true);
    } else if (data.status === 'stopped') {
        updateDetectionStatus(false);
    }
});

socket.on('video_frame', (data) => {
    if (!isDetecting) return;
    
    // Update video feed
    videoFeed.src = 'data:image/jpeg;base64,' + data.image;
    videoFeed.style.display = 'block';
    videoPlaceholder.style.display = 'none';
    
    // Update detection statistics
    updateDetectionStats(data.detections);
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateConnectionStatus(false);
    updateDetectionStatus(false);
});

// Handle window beforeunload
window.addEventListener('beforeunload', () => {
    if (isDetecting) {
        socket.emit('stop_detection');
    }
});
