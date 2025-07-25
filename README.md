# 🤖 Google ADK Deepfake Detection Agent

A sophisticated conversational AI agent that detects deepfakes in images and synthetic voices in audio files using Google's Agent Development Kit (ADK) with Dialogflow CX integration.

## ✨ Features

- **🖼️ Image Deepfake Detection**: Advanced AI-generated image detection
- **🎵 Audio Deepfake Detection**: Synthetic voice detection and analysis  
- **💬 Conversational Interface**: Natural language interaction via Dialogflow CX
- **🌐 Web Interface**: User-friendly web UI for file uploads and chat
- **💻 Terminal Interface**: Command-line interaction for developers
- **💰 Cost Optimized**: Local processing mode to avoid cloud charges
- **🔍 Real-time Analysis**: Instant detection results with confidence scores

## 🏗️ Architecture

```
Project-JER/
├── google_agent/           # Google ADK Integration
│   ├── adk_local.py       # Local web server (cost-optimized)
│   ├── adk_terminal.py    # Terminal interface
│   ├── adk_web_fixed.py   # Web interface with webhook support
│   └── templates/         # HTML templates
├── backend/               # ML Detection Backend
│   ├── test_main.py      # Flask API server
│   └── main.py           # Core detection logic
├── agent/                # Original agent implementation
├── models/               # ML model storage
└── deploy/              # Deployment configurations
```

## 🚀 Quick Start

### Prerequisites

1. Python 3.8+ installed
2. Virtual environment activated:
   ```bash
   .\projectjer\Scripts\activate  # Windows
   # or
   source projectjer/bin/activate  # Linux/Mac
   ```

### Option 1: Local Web Interface (Recommended) 💰

**Cost-optimized version with no cloud charges:**

```bash
# 1. Navigate to Google agent directory
cd google_agent

# 2. Start the local web server
python adk_local.py
```

Open http://localhost:5000 in your browser to access the web interface.

### Option 2: Terminal Interface

```bash
# Navigate to Google agent directory
cd google_agent

# Run terminal interface
python adk_terminal.py
```

### Option 3: Full Backend + Web Interface

```bash
# Terminal 1: Start ML backend
cd backend
python test_main.py

# Terminal 2: Start web interface  
cd google_agent
python adk_web_fixed.py
```
## 🔧 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Project-JER.git
   cd Project-JER
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download ML models** (if using full backend):
   ```bash
   # Models will be automatically downloaded on first run
   cd backend
   python test_main.py
   ```

## 💡 Usage Examples

### Web Interface

1. **Upload Files**: Drag and drop or select images/audio files
2. **Chat**: Ask questions about deepfake detection
3. **Analyze**: Get instant results with confidence scores

### Terminal Interface

```bash
$ python adk_terminal.py
🤖 Google ADK Terminal Interface
💻 Mode: Local Processing

Enter your message (or 'quit' to exit): analyze my image
📁 Please provide the file path: ./test_image.jpg
🔍 Analyzing image...
✅ Result: Real/Authentic (87.3% confidence)
```

### Supported File Types

- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`
- **Audio**: `.wav`, `.mp3`, `.flac`, `.ogg`, `.m4a`

## 🔬 Detection Technology

### Image Analysis
- **AI Pattern Recognition**: Detects artificial patterns in pixel distribution
- **Compression Analysis**: Identifies compression artifacts typical of generated content
- **Texture Analysis**: Analyzes realistic vs synthetic textures

### Audio Analysis  
- **Voice Synthesis Detection**: Identifies unnatural phoneme transitions
- **Spectral Analysis**: Analyzes frequency patterns typical of TTS systems
- **Prosody Analysis**: Detects natural vs artificial speech patterns

## 🌐 Google ADK Integration

This project leverages Google's Agent Development Kit (ADK) with:

- **Dialogflow CX**: Advanced conversational AI
- **Cloud Run**: Scalable webhook deployment (optional)
- **Natural Language Processing**: Intent recognition and response generation
- **Multi-modal Support**: Text, image, and audio processing

## 💰 Cost Optimization

The project includes a **local processing mode** (`adk_local.py`) that:

- ✅ Eliminates all cloud charges
- ✅ Provides same functionality as cloud version
- ✅ Uses intelligent mock detection for demonstration
- ✅ Includes enhanced filename-based analysis

## 📁 Project Structure

```
Project-JER/
├── 📁 google_agent/           # Google ADK Integration
│   ├── 🐍 adk_local.py       # Local web server (recommended)
│   ├── 🐍 adk_terminal.py    # Terminal interface  
│   ├── 🐍 adk_web_fixed.py   # Full web interface
│   ├── 📁 templates/         # HTML templates
│   └── 📄 *.md              # Documentation files
├── 📁 backend/               # ML Detection Backend
│   ├── 🐍 test_main.py      # Flask API server
│   └── 🐍 main.py           # Core detection logic
├── 📁 agent/                # Original agent implementation
├── 📁 models/               # ML model storage
├── 📁 deploy/               # Deployment configurations
├── 🐳 Dockerfile            # Container configuration
├── 📋 requirements.txt      # Python dependencies
└── 📖 README.md            # This file
```

## 🔧 Configuration

### Environment Variables
```bash
# Optional: For cloud deployment
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
```

### Local Configuration
All local processing requires no additional configuration - just run and use!

## 🚀 Deployment

### Local Development
```bash
python google_agent/adk_local.py
```

### Cloud Deployment (Optional)
```bash
# Build and deploy to Google Cloud Run
./deploy.sh
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For issues and questions:

1. Check the [Documentation](google_agent/INTEGRATION_SUMMARY.py)
2. Review [Deployment Guide](google_agent/DEPLOYMENT_SUMMARY.md)
3. Open an issue on GitHub

## 🏆 Acknowledgments

- Google Cloud AI for Dialogflow CX
- Hugging Face for transformer models
- Flask community for web framework
- Open source ML community

---

**⚡ Quick Demo**: Run `python google_agent/adk_local.py` and visit http://localhost:5000 to try it now!
- **Input**: Image (.jpg, .png) or Audio (.wav, .mp3, .flac) files
- **Output**: JSON with `type`, `result`, `confidence`, `explanation`

## Technical Implementation
- **Image Model**: Hugging Face transformers pipeline with CPU inference
- **Audio Analysis**: MFCC variance, spectral centroid, and zero-crossing rate features
- **File Handling**: PIL for images, librosa for audio processing
- **Web Framework**: Flask with file upload support
- **Conversational AI**: Google Dialogflow CX with webhook fulfillment
- **Cloud Deployment**: Google Cloud Run with container orchestration
- **Session Management**: Persistent conversation state and history tracking

## Google Dialogflow CX Features ⭐
- **Natural Language Understanding**: Intent recognition and entity extraction
- **Conversation Management**: Session-based dialog state management  
- **Webhook Integration**: Real-time fulfillment with ML model inference
- **Multi-modal Input**: Text and file upload support
- **Cloud Scalability**: Auto-scaling webhook deployment on Cloud Run
- **Mock Fallback**: Graceful degradation when Google Cloud services unavailable

## Next Steps
- ✅ **Google Agent Development Kit Integration Complete** 
- Deploy webhook to Google Cloud Run
- Create production Dialogflow CX agent in Google Cloud Console
- Configure service account credentials for production
- Add Google Cloud Storage integration for file handling
- Implement advanced conversation flows and intents
# Project-JER