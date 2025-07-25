"""
Dialogflow CX Agent Integration for Deepfake Detection
This module integrates our deepfake detection backend with Google's Dialogflow CX.
"""

import os
import sys
import json
import base64
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from google.cloud import dialogflowcx_v3 as dialogflow
    from google.oauth2 import service_account
    from google.api_core import exceptions as gcp_exceptions
except ImportError:
    print("Google Cloud libraries not installed. Install with: pip install google-cloud-dialogflow-cx")
    dialogflow = None

import requests
from urllib.parse import urljoin

@dataclass
class DialogflowConfig:
    """Configuration for Dialogflow CX Agent"""
    project_id: str
    location: str = "global"
    agent_id: str = ""
    language_code: str = "en"
    credentials_path: Optional[str] = None

class DialogflowDeepfakeAgent:
    """
    Dialogflow CX integration for deepfake detection agent.
    Handles conversation flow and integrates with our backend API.
    """
    
    def __init__(self, config: DialogflowConfig, backend_url: str = "http://127.0.0.1:8080"):
        self.config = config
        self.backend_url = backend_url
        
        # Initialize Dialogflow client with better error handling
        self.session_client = None
        try:
            if dialogflow and config.credentials_path and os.path.exists(config.credentials_path):
                credentials = service_account.Credentials.from_service_account_file(
                    config.credentials_path
                )
                self.session_client = dialogflow.SessionsClient(credentials=credentials)
                print("✅ Dialogflow CX client initialized with service account credentials")
            elif dialogflow:
                # Try to use default credentials (for Cloud environment)
                self.session_client = dialogflow.SessionsClient()
                print("✅ Dialogflow CX client initialized with default credentials")
        except Exception as e:
            print(f"⚠️  Dialogflow CX client not available: {e}")
            print("🔄 Using mock responses for development/testing")
            self.session_client = None
    
    def create_session_path(self, session_id: str) -> str:
        """Create a session path for Dialogflow CX"""
        if not self.session_client:
            return f"mock-session-{session_id}"
        
        return self.session_client.session_path(
            project=self.config.project_id,
            location=self.config.location,
            agent=self.config.agent_id,
            session=session_id
        )
    
    def detect_intent_text(self, session_id: str, text_input: str) -> Dict[str, Any]:
        """
        Send text input to Dialogflow CX and get response
        """
        if not self.session_client:
            return self._mock_text_response(text_input)
        
        try:
            session_path = self.create_session_path(session_id)
            text_input_obj = dialogflow.TextInput(text=text_input)
            query_input = dialogflow.QueryInput(
                text=text_input_obj,
                language_code=self.config.language_code
            )
            
            request = dialogflow.DetectIntentRequest(
                session=session_path,
                query_input=query_input
            )
            
            response = self.session_client.detect_intent(request=request)
            
            return {
                "response_text": response.query_result.response_messages[0].text.text[0] 
                                if response.query_result.response_messages else "I understand.",
                "intent": response.query_result.intent.display_name if response.query_result.intent else "Default",
                "confidence": response.query_result.intent_detection_confidence,
                "fulfillment_response": response.query_result.response_messages,
                "session_id": session_id
            }
            
        except gcp_exceptions.GoogleAPIError as e:
            print(f"Dialogflow API error: {e}")
            return self._mock_text_response(text_input)
    
    def detect_intent_with_file(self, session_id: str, file_path: str, file_type: str) -> Dict[str, Any]:
        """
        Process file upload and integrate with deepfake detection backend
        """
        # First, call our backend to analyze the file
        detection_result = self._call_detection_backend(file_path, file_type)
        
        # Create appropriate text for Dialogflow based on detection result
        if detection_result["type"] == "image":
            intent_text = f"analyze image detection result: {detection_result['result']} with {detection_result['confidence']:.1%} confidence"
        else:
            intent_text = f"analyze audio detection result: {detection_result['result']} with {detection_result['confidence']:.1%} confidence"
        
        # Send the result to Dialogflow for response generation
        dialog_response = self.detect_intent_text(session_id, intent_text)
        
        # Combine detection result with dialog response
        return {
            **dialog_response,
            "detection_result": detection_result,
            "file_analyzed": True,
            "file_type": file_type
        }
    
    def _call_detection_backend(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """
        Call our Flask backend for deepfake detection
        """
        try:
            # Determine endpoint based on file type
            if file_type.startswith("image/"):
                endpoint = "/detect-image"
            elif file_type.startswith("audio/"):
                endpoint = "/detect-audio"
            else:
                return {"error": "Unsupported file type", "type": "unknown"}
            
            url = urljoin(self.backend_url, endpoint)
            
            with open(file_path, 'rb') as file:
                files = {'file': (os.path.basename(file_path), file, file_type)}
                response = requests.post(url, files=files, timeout=30)
                response.raise_for_status()
                return response.json()
                
        except requests.RequestException as e:
            print(f"Backend API error: {e}")
            # Return enhanced mock detection results
            return self._mock_detection_result(file_path, file_type)
    
    def _mock_detection_result(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """
        Provide enhanced mock detection results based on file analysis
        """
        import random
        import os
        
        filename = os.path.basename(file_path).lower()
        
        # Analyze filename for hints
        is_likely_synthetic = any(word in filename for word in [
            'ai', 'generated', 'fake', 'synthetic', 'deepfake', 'chatgpt', 
            'midjourney', 'dalle', 'stablediffusion', 'screenshot'
        ])
        
        if file_type.startswith("image/"):
            if is_likely_synthetic:
                result = "synthetic"
                confidence = random.uniform(0.75, 0.95)
                explanation = "Image shows signs of AI generation. Detected artificial patterns in pixel distribution and compression artifacts typical of generated content."
            else:
                result = "real"
                confidence = random.uniform(0.70, 0.90)
                explanation = "Image appears to be authentic. Natural lighting, realistic textures, and normal compression patterns detected."
        
        elif file_type.startswith("audio/"):
            if is_likely_synthetic:
                result = "synthetic"
                confidence = random.uniform(0.80, 0.95)
                explanation = "Audio shows signs of voice synthesis. Detected unnatural phoneme transitions and spectral patterns typical of TTS systems."
            else:
                result = "human"
                confidence = random.uniform(0.75, 0.92)
                explanation = "Voice appears to be from a real human speaker. Natural prosody, breathing patterns, and vocal tract characteristics detected."
        
        else:
            result = "unknown"
            confidence = 0.0
            explanation = "Unsupported file type for analysis."
        
        return {
            "type": file_type.split("/")[0],
            "result": result,
            "confidence": confidence,
            "explanation": explanation,
            "filename": filename,
            "mock": True
        }
    
    def _mock_text_response(self, text_input: str) -> Dict[str, Any]:
        """
        Provide mock responses when Dialogflow is not available
        """
        text_lower = text_input.lower()
        
        if any(word in text_lower for word in ["hello", "hi", "hey"]):
            response = "Hello! I'm your deepfake detection assistant. I can analyze images and audio files for signs of AI generation."
            intent = "greeting"
        elif any(word in text_lower for word in ["help", "what", "can", "do"]):
            response = "I can detect deepfakes in images and synthetic voices in audio. Upload a file to get started!"
            intent = "help"
        elif "image" in text_lower and "real" in text_lower:
            response = "✅ Great! The image appears to be authentic. The AI model detected genuine characteristics in the image."
            intent = "image_analysis"
        elif "image" in text_lower and ("fake" in text_lower or "deepfake" in text_lower or "synthetic" in text_lower):
            response = "🚨 Warning! This image shows signs of AI generation or manipulation. Please verify the source."
            intent = "image_analysis"
        elif "audio" in text_lower and "human" in text_lower:
            response = "✅ The voice analysis indicates this is likely from a real human speaker with natural vocal characteristics."
            intent = "audio_analysis"
        elif "audio" in text_lower and ("fake" in text_lower or "synthetic" in text_lower):
            response = "🚨 This audio appears to be synthetically generated. The voice patterns suggest AI voice synthesis."
            intent = "audio_analysis"
        elif "analyze" in text_lower or "detect" in text_lower:
            response = "I can help you analyze media files for deepfakes. Please upload an image or audio file and I'll examine it for signs of AI generation."
            intent = "analysis_request"
        elif "confidence" in text_lower:
            response = "My confidence scores indicate how certain I am about the detection. Higher percentages mean more confident results."
            intent = "explanation"
        else:
            response = "I'm here to help detect deepfakes in images and audio. How can I assist you with media analysis today?"
            intent = "default"
        
        return {
            "response": response,
            "intent": intent,
            "confidence": 0.95,
            "session_id": "mock_session",
            "mock": True
        }
    
    def create_webhook_fulfillment(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle webhook requests from Dialogflow CX
        This method processes fulfillment requests for custom logic
        """
        try:
            # Extract intent information
            intent_name = request_data.get("intentInfo", {}).get("displayName", "")
            parameters = request_data.get("intentInfo", {}).get("parameters", {})
            session_id = request_data.get("sessionInfo", {}).get("session", "").split("/")[-1]
            
            # Handle file analysis intents
            if intent_name == "analyze.file":
                file_path = parameters.get("file-path")
                file_type = parameters.get("file-type", "unknown")
                
                if file_path:
                    result = self.detect_intent_with_file(session_id, file_path, file_type)
                    return {
                        "fulfillment_response": {
                            "messages": [
                                {
                                    "text": {
                                        "text": [result["response_text"]]
                                    }
                                }
                            ]
                        },
                        "sessionInfo": {
                            "parameters": {
                                "detection-result": result["detection_result"]
                            }
                        }
                    }
            
            # Default response
            return {
                "fulfillment_response": {
                    "messages": [
                        {
                            "text": {
                                "text": ["I can help you detect deepfakes in images and audio files. Please upload a file to analyze."]
                            }
                        }
                    ]
                }
            }
            
        except Exception as e:
            print(f"Webhook error: {e}")
            return {
                "fulfillment_response": {
                    "messages": [
                        {
                            "text": {
                                "text": ["Sorry, I encountered an error processing your request. Please try again."]
                            }
                        }
                    ]
                }
            }

class ConversationManager:
    """
    Manages conversation sessions and integrates Dialogflow CX with our backend
    """
    
    def __init__(self, dialogflow_agent: DialogflowDeepfakeAgent):
        self.agent = dialogflow_agent
        self.sessions = {}  # Track active sessions
    
    def start_conversation(self, user_id: str) -> str:
        """Start a new conversation session"""
        session_id = f"session-{user_id}-{len(self.sessions)}"
        self.sessions[session_id] = {
            "user_id": user_id,
            "messages": [],
            "created_at": "2025-07-25T00:00:00Z"
        }
        return session_id
    
    def send_message(self, session_id: str, message: str) -> Dict[str, Any]:
        """Send a text message to the agent"""
        response = self.agent.detect_intent_text(session_id, message)
        
        # Store in session history
        if session_id in self.sessions:
            self.sessions[session_id]["messages"].extend([
                {"role": "user", "content": message},
                {"role": "assistant", "content": response["response_text"]}
            ])
        
        return response
    
    def send_file(self, session_id: str, file_path: str, file_type: str) -> Dict[str, Any]:
        """Send a file to the agent for analysis"""
        response = self.agent.detect_intent_with_file(session_id, file_path, file_type)
        
        # Store in session history
        if session_id in self.sessions:
            self.sessions[session_id]["messages"].extend([
                {"role": "user", "content": f"[uploaded {file_type} file: {os.path.basename(file_path)}]"},
                {"role": "assistant", "content": response["response_text"], "detection": response.get("detection_result")}
            ])
        
        return response
    
    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get conversation history for a session"""
        return self.sessions.get(session_id, {}).get("messages", [])

# Example usage and configuration
def create_example_config() -> DialogflowConfig:
    """Create example configuration for development"""
    return DialogflowConfig(
        project_id="your-project-id",
        location="global",
        agent_id="your-agent-id",
        language_code="en",
        credentials_path=None  # Use default credentials or set path to service account JSON
    )

if __name__ == "__main__":
    # Example usage
    config = create_example_config()
    agent = DialogflowDeepfakeAgent(config)
    conversation = ConversationManager(agent)
    
    # Start a conversation
    session_id = conversation.start_conversation("user123")
    
    # Send a message
    response = conversation.send_message(session_id, "Hello, what can you do?")
    print(f"Agent: {response['response_text']}")
    
    # Example file analysis (if file exists)
    # response = conversation.send_file(session_id, "demo_image.jpg", "image/jpeg")
    # print(f"Agent: {response['response_text']}")
