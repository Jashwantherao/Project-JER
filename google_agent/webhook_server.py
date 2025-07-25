"""
Google Cloud Run Webhook for Dialogflow CX
This Flask app serves as a webhook endpoint for Dialogflow CX fulfillment.
"""

import os
import sys
import json
import tempfile
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google_agent.dialogflow_agent import DialogflowDeepfakeAgent, DialogflowConfig

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize Dialogflow agent
config = DialogflowConfig(
    project_id=os.getenv('GOOGLE_CLOUD_PROJECT', 'your-project-id'),
    location=os.getenv('DIALOGFLOW_LOCATION', 'global'),
    agent_id=os.getenv('DIALOGFLOW_AGENT_ID', 'your-agent-id'),
    language_code=os.getenv('DIALOGFLOW_LANGUAGE', 'en'),
    credentials_path=os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
)

# Backend URL (could be the same Cloud Run service or separate)
backend_url = os.getenv('BACKEND_URL', 'http://127.0.0.1:8080')
agent = DialogflowDeepfakeAgent(config, backend_url)

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Dialogflow CX Deepfake Detection Webhook",
        "version": "1.0.0"
    })

@app.route('/webhook', methods=['POST'])
def dialogflow_webhook():
    """
    Main webhook endpoint for Dialogflow CX fulfillment
    """
    try:
        request_data = request.get_json()
        
        # Log the request for debugging
        print(f"Webhook request: {json.dumps(request_data, indent=2)}")
        
        # Process the fulfillment request
        response = agent.create_webhook_fulfillment(request_data)
        
        # Log the response for debugging
        print(f"Webhook response: {json.dumps(response, indent=2)}")
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({
            "fulfillment_response": {
                "messages": [
                    {
                        "text": {
                            "text": ["Sorry, I encountered an error. Please try again."]
                        }
                    }
                ]
            }
        }), 200  # Return 200 to avoid Dialogflow retries

@app.route('/detect-file', methods=['POST'])
def detect_file():
    """
    Direct file upload endpoint for testing
    This can be called directly or from Dialogflow rich responses
    """
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        # Determine file type
        if file_extension in ['jpg', 'jpeg', 'png']:
            file_type = f"image/{file_extension}"
        elif file_extension in ['wav', 'mp3', 'flac']:
            file_type = f"audio/{file_extension}"
        else:
            return jsonify({"error": "Unsupported file type"}), 400
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_extension}') as tmp_file:
            file.save(tmp_file.name)
            tmp_path = tmp_file.name
        
        try:
            # Analyze the file
            session_id = request.form.get('session_id', 'direct-upload')
            result = agent.detect_intent_with_file(session_id, tmp_path, file_type)
            
            # Clean up temporary file
            os.unlink(tmp_path)
            
            return jsonify(result)
            
        except Exception as e:
            # Clean up temporary file on error
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise e
            
    except Exception as e:
        print(f"File detection error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """
    Direct chat endpoint for testing
    This provides a simple REST API for text conversations
    """
    try:
        data = request.get_json()
        message = data.get('message', '')
        session_id = data.get('session_id', 'direct-chat')
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        # Process the message
        response = agent.detect_intent_text(session_id, message)
        
        return jsonify({
            "response": response["response_text"],
            "intent": response["intent"],
            "confidence": response["confidence"],
            "session_id": session_id
        })
        
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({"error": "File too large. Maximum size is 16MB."}), 413

@app.errorhandler(Exception)
def handle_exception(e):
    """Global exception handler"""
    print(f"Unhandled exception: {e}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # For local development
    port = int(os.environ.get('PORT', 8081))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"Starting Dialogflow CX Webhook server on port {port}")
    print(f"Backend URL: {backend_url}")
    print(f"Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
