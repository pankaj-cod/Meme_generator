# Deployment Guide - Face Meme Generator

This guide covers multiple deployment options for your Face Meme Generator application.

## Quick Deployment Options

### Option 1: Render (Recommended - Free Tier Available)

Render is perfect for Flask apps and offers a free tier.

#### Steps:

1. **Create `render.yaml`** (already included in this guide below)

2. **Sign up at [Render](https://render.com)**

3. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `https://github.com/pankaj-cod/Meme_generator`
   - Render will auto-detect it's a Python app

4. **Configure Settings**
   - **Name**: `face-meme-generator`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free

5. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment

#### Free Tier Limitations:
- App sleeps after 15 minutes of inactivity
- 750 hours/month free
- Slower cold starts

---

### Option 2: Railway (Easy & Fast)

Railway offers simple deployment with generous free tier.

#### Steps:

1. **Sign up at [Railway](https://railway.app)**

2. **New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `pankaj-cod/Meme_generator`

3. **Configure**
   - Railway auto-detects Python
   - Add environment variable: `PORT=5001`
   - Deploy automatically starts

4. **Get URL**
   - Click on deployment
   - Copy the generated URL

---

### Option 3: PythonAnywhere (Simple, Free Tier)

Good for beginners, free tier available.

#### Steps:

1. **Sign up at [PythonAnywhere](https://www.pythonanywhere.com)**

2. **Upload Code**
   - Go to "Files" tab
   - Upload your project or clone from GitHub:
   ```bash
   git clone https://github.com/pankaj-cod/Meme_generator.git
   ```

3. **Create Virtual Environment**
   ```bash
   cd Meme_generator
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration" → Python 3.10
   - Set source code directory: `/home/yourusername/Meme_generator`
   - Set virtualenv: `/home/yourusername/Meme_generator/venv`

5. **Edit WSGI file**
   - Click on WSGI configuration file
   - Replace contents with:
   ```python
   import sys
   path = '/home/yourusername/Meme_generator'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

6. **Reload** and visit your URL

---

### Option 4: Heroku (Popular, Paid)

> [!NOTE]
> Heroku no longer offers a free tier, but it's still popular for production apps.

#### Steps:

1. **Install Heroku CLI**
   ```bash
   brew tap heroku/brew && brew install heroku
   ```

2. **Login**
   ```bash
   heroku login
   ```

3. **Create App**
   ```bash
   cd /Users/pankaj/Desktop/ML_Project
   heroku create face-meme-generator
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Open App**
   ```bash
   heroku open
   ```

---

### Option 5: Google Cloud Run (Scalable, Free Tier)

Serverless deployment with generous free tier.

#### Steps:

1. **Install Google Cloud SDK**
   ```bash
   brew install google-cloud-sdk
   ```

2. **Initialize**
   ```bash
   gcloud init
   gcloud auth login
   ```

3. **Deploy**
   ```bash
   cd /Users/pankaj/Desktop/ML_Project
   gcloud run deploy face-meme-generator \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

---

## Required Files for Deployment

### 1. Procfile (for Heroku/Render)

Create `Procfile` in project root:
```
web: gunicorn app:app
```

### 2. runtime.txt (specify Python version)

Create `runtime.txt`:
```
python-3.11.0
```

### 3. Update requirements.txt

Add gunicorn for production:
```
flask>=3.0.0
opencv-python>=4.8.0
numpy>=1.26.0
Pillow>=10.0.0
gunicorn>=21.0.0
```

### 4. Dockerfile (for containerized deployment)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]
```

### 5. .dockerignore

Create `.dockerignore`:
```
venv/
__pycache__/
*.pyc
.git/
.gitignore
static/uploads/*
static/memes/*
```

### 6. render.yaml (for Render)

Create `render.yaml`:
```yaml
services:
  - type: web
    name: face-meme-generator
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

---

## Environment Variables

For production, you may want to set:

```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
MAX_CONTENT_LENGTH=16777216  # 16MB
```

---

## Pre-Deployment Checklist

- [ ] Update `app.py` to use environment port:
  ```python
  port = int(os.environ.get('PORT', 5001))
  app.run(host='0.0.0.0', port=port)
  ```

- [ ] Set `debug=False` for production
- [ ] Add gunicorn to requirements.txt
- [ ] Create Procfile
- [ ] Test locally with gunicorn:
  ```bash
  gunicorn app:app
  ```

- [ ] Ensure static files are properly configured
- [ ] Add error logging
- [ ] Set up HTTPS (most platforms do this automatically)

---

## Recommended: Render Deployment (Easiest)

For your first deployment, I recommend **Render** because:

✅ Free tier available
✅ Automatic HTTPS
✅ Easy GitHub integration
✅ Auto-deploys on git push
✅ Good for Python apps
✅ No credit card required for free tier

**Quick Start:**
1. Push the required files (I'll create them for you)
2. Go to render.com
3. Connect GitHub
4. Select your repo
5. Click deploy
6. Done! 🎉

---

## Monitoring & Maintenance

After deployment:

1. **Monitor Logs**: Check application logs regularly
2. **Set Up Alerts**: Configure uptime monitoring (e.g., UptimeRobot)
3. **Backup**: Regularly backup generated memes if needed
4. **Updates**: Keep dependencies updated
5. **Security**: Regularly update packages for security patches

---

## Troubleshooting

### Common Issues:

**Port Binding Error**
```python
# Use environment PORT variable
port = int(os.environ.get('PORT', 5001))
```

**OpenCV Import Error**
- Ensure system dependencies are installed (see Dockerfile)
- Use `opencv-python-headless` for serverless environments

**Memory Issues**
- Limit image upload size
- Clean up old uploads/memes periodically
- Use smaller instance if on free tier

**Slow Cold Starts**
- Upgrade to paid tier
- Use keep-alive services (e.g., cron-job.org to ping your app)

---

## Cost Comparison

| Platform | Free Tier | Paid Starting | Best For |
|----------|-----------|---------------|----------|
| Render | 750 hrs/mo | $7/mo | Hobby projects |
| Railway | $5 credit/mo | $5/mo usage | Quick deploys |
| PythonAnywhere | Limited | $5/mo | Beginners |
| Heroku | None | $7/mo | Production |
| Google Cloud Run | 2M requests/mo | Pay per use | Scalability |

---

## Next Steps

1. Choose a deployment platform
2. I'll create the necessary deployment files
3. Follow the platform-specific steps above
4. Share your deployed URL! 🚀

Need help with any specific platform? Let me know!
