
"""
Flask backend for Face Meme Generator
"""
from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
import uuid
from face_analyzer import FaceAnalyzer
from meme_generator import MemeGenerator

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MEME_FOLDER'] = 'static/memes'

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['MEME_FOLDER'], exist_ok=True)

# Initialize ML models
face_analyzer = FaceAnalyzer()
meme_generator = MemeGenerator()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and process the image"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF)'}), 400
    
    try:
        # Save uploaded file with unique name
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Detect faces
        face_count, _ = face_analyzer.detect_faces(filepath)
        
        if face_count == 0:
            return jsonify({
                'error': 'No faces detected in the image. Please upload an image with a visible face.'
            }), 400
        
        # Analyze emotion
        emotion_result = face_analyzer.analyze_emotion(filepath)
        
        if not emotion_result['success']:
            return jsonify({
                'error': 'Could not analyze facial expression. Please try another image.'
            }), 400
        
        # Generate meme
        meme_filename = f"meme_{unique_filename}"
        meme_path = os.path.join(app.config['MEME_FOLDER'], meme_filename)
        
        generated_meme = meme_generator.generate_meme(
            filepath, 
            emotion_result['dominant_emotion'],
            meme_path
        )
        
        if not generated_meme:
            return jsonify({'error': 'Failed to generate meme'}), 500
        
        # Get emotion description
        emotion_desc = face_analyzer.get_emotion_description(emotion_result['dominant_emotion'])
        
        return jsonify({
            'success': True,
            'face_count': face_count,
            'emotion': emotion_result['dominant_emotion'],
            'emotion_description': emotion_desc,
            'confidence': round(emotion_result['confidence'], 2),
            'emotion_scores': {k: round(v, 2) for k, v in emotion_result['emotion_scores'].items()},
            'original_image': f'/static/uploads/{unique_filename}',
            'meme_image': f'/static/memes/{meme_filename}'
        })
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/static/<path:path>')
def send_static(path):
    """Serve static files"""
    return send_from_directory('static', path)

if __name__ == '__main__':
    print("🎭 Face Meme Generator is starting...")
    print("📊 Loading ML models (this may take a moment)...")
    
    # Use environment PORT variable for deployment platforms
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    print(f"🚀 Server will be available at http://localhost:{port}")
    app.run(debug=debug, host='0.0.0.0', port=port)
