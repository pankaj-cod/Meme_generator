// DOM Elements
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const cameraBtn = document.getElementById('cameraBtn');
const cameraSection = document.getElementById('cameraSection');
const cameraVideo = document.getElementById('cameraVideo');
const cameraCanvas = document.getElementById('cameraCanvas');
const captureBtn = document.getElementById('captureBtn');
const closeCameraBtn = document.getElementById('closeCameraBtn');
const loading = document.getElementById('loading');
const error = document.getElementById('error');
const errorMessage = document.getElementById('errorMessage');
const results = document.getElementById('results');

let currentMemeUrl = '';
let cameraStream = null;

// Event Listeners
uploadBtn.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', handleFileSelect);
cameraBtn.addEventListener('click', openCamera);
captureBtn.addEventListener('click', capturePhoto);
closeCameraBtn.addEventListener('click', closeCamera);

// Drag and drop
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('dragover');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        handleFileSelect();
    }
});

uploadBox.addEventListener('click', (e) => {
    if (e.target !== uploadBtn && e.target !== cameraBtn) {
        fileInput.click();
    }
});

// Camera Functions
async function openCamera() {
    try {
        // Request camera access
        cameraStream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: 'user',
                width: { ideal: 1280 },
                height: { ideal: 720 }
            }
        });

        // Show camera section, hide upload
        uploadBox.parentElement.style.display = 'none';
        cameraSection.style.display = 'block';

        // Set video stream
        cameraVideo.srcObject = cameraStream;

    } catch (err) {
        console.error('Camera error:', err);
        showError('Could not access camera. Please ensure camera permissions are granted.');
    }
}

function capturePhoto() {
    // Set canvas size to match video
    cameraCanvas.width = cameraVideo.videoWidth;
    cameraCanvas.height = cameraVideo.videoHeight;

    // Draw current video frame to canvas
    const ctx = cameraCanvas.getContext('2d');
    ctx.drawImage(cameraVideo, 0, 0);

    // Convert canvas to blob
    cameraCanvas.toBlob((blob) => {
        if (blob) {
            // Create a file from the blob
            const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });

            // Close camera
            closeCamera();

            // Upload the captured image
            uploadImage(file);
        }
    }, 'image/jpeg', 0.95);
}

function closeCamera() {
    // Stop camera stream
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }

    // Hide camera section, show upload
    cameraSection.style.display = 'none';
    uploadBox.parentElement.style.display = 'block';
}

function handleFileSelect() {
    const file = fileInput.files[0];

    if (!file) return;

    // Validate file type
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif'];
    if (!validTypes.includes(file.type)) {
        showError('Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF)');
        return;
    }

    // Validate file size (16MB)
    if (file.size > 16 * 1024 * 1024) {
        showError('File too large. Maximum size is 16MB');
        return;
    }

    uploadImage(file);
}

async function uploadImage(file) {
    // Hide all sections
    uploadBox.parentElement.style.display = 'none';
    cameraSection.style.display = 'none';
    error.style.display = 'none';
    results.style.display = 'none';
    loading.style.display = 'block';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Upload failed');
        }

        displayResults(data);

    } catch (err) {
        showError(err.message);
    }
}

function displayResults(data) {
    loading.style.display = 'none';
    results.style.display = 'block';

    // Set emotion info
    document.getElementById('emotionValue').textContent = data.emotion;
    document.getElementById('emotionDescription').textContent = data.emotion_description;
    document.getElementById('confidenceValue').textContent = data.confidence;
    document.getElementById('faceCount').textContent = data.face_count;

    // Display emotion scores
    const scoresGrid = document.getElementById('scoresGrid');
    scoresGrid.innerHTML = '';

    // Sort emotions by score
    const sortedEmotions = Object.entries(data.emotion_scores)
        .sort(([, a], [, b]) => b - a);

    sortedEmotions.forEach(([emotion, score]) => {
        const scoreItem = document.createElement('div');
        scoreItem.className = 'score-item';
        scoreItem.innerHTML = `
            <span class="score-label">${emotion}</span>
            <span class="score-value">${score}%</span>
        `;
        scoresGrid.appendChild(scoreItem);
    });

    // Display images
    document.getElementById('originalImage').src = data.original_image;
    document.getElementById('memeImage').src = data.meme_image;
    currentMemeUrl = data.meme_image;

    // Scroll to results
    results.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function showError(message) {
    loading.style.display = 'none';
    uploadBox.parentElement.style.display = 'none';
    cameraSection.style.display = 'none';
    results.style.display = 'none';
    error.style.display = 'block';
    errorMessage.textContent = message;

    error.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function resetUpload() {
    fileInput.value = '';
    closeCamera(); // Close camera if open
    uploadBox.parentElement.style.display = 'block';
    loading.style.display = 'none';
    error.style.display = 'none';
    results.style.display = 'none';

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function downloadMeme() {
    if (!currentMemeUrl) return;

    const link = document.createElement('a');
    link.href = currentMemeUrl;
    link.download = 'my-meme.jpg';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
