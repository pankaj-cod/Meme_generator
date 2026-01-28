# Face Meme Generator 🎭

An ML-powered web application that analyzes facial expressions and automatically generates contextual memes based on detected emotions.

## Features

- **Face Detection**: Uses OpenCV Haar Cascade for reliable face detection
- **Emotion Analysis**: Analyzes facial expressions (happy, sad, angry, surprise, fear, disgust, neutral)
- **Automatic Meme Generation**: Generates appropriate memes based on detected emotions
- **Web Interface**: Simple and intuitive web UI for uploading images
- **Real-time Processing**: Quick analysis and meme generation

## Technologies Used

- **Backend**: Flask (Python)
- **Face Detection**: OpenCV Haar Cascade
- **Emotion Analysis**: Image-based analysis (upgradeable to deep learning models)
- **Image Processing**: OpenCV, Pillow
- **Frontend**: HTML, CSS, JavaScript

## Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Upload an image with a face and watch the magic happen!

## Project Structure

```
ML_Project/
├── app.py                 # Flask backend
├── face_analyzer.py       # Face detection and emotion analysis
├── meme_generator.py      # Meme generation logic
├── requirements.txt       # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   ├── js/
│   │   └── main.js       # Frontend logic
│   └── uploads/          # Uploaded images
├── templates/
│   └── index.html        # Main page
└── meme_templates/       # Meme template images
```

## How It Works

1. User uploads an image through the web interface
2. MediaPipe detects faces in the image
3. DeepFace analyzes the facial expression and determines the emotion
4. The system selects an appropriate meme template based on the emotion
5. A custom meme is generated with relevant text
6. The meme is displayed to the user

## License

MIT License
