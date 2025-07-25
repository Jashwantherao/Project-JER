# agent/main.py
"""
Conversational Agent using Google Agent Development Kit (ADK)
This agent interacts with users, accepts image/audio input, and calls backend endpoints for deepfake detection.
"""

import requests
import json

BACKEND_URL = "http://127.0.0.1:8080"  # Our tested backend URL

class DeepfakeDetectionAgent:
    def __init__(self, name: str):
        self.name = name
        print(f"Initializing {self.name} agent...")

    def process_message(self, message_text: str = None, file_path: str = None, file_type: str = None):
        """
        Process user input and return appropriate response
        """
        try:
            if file_path and file_type:
                if file_type.startswith("image/"):
                    result = self.detect_image(file_path)
                    return self.format_result(result)
                elif file_type.startswith("audio/"):
                    result = self.detect_audio(file_path)
                    return self.format_result(result)
                else:
                    return "Sorry, I can only process image and audio files."
            
            elif message_text:
                if "photo" in message_text.lower() or "image" in message_text.lower():
                    return "Please upload an image (jpg/png) for deepfake detection."
                elif "voice" in message_text.lower() or "audio" in message_text.lower():
                    return "Please upload an audio file (mp3/wav/flac) for voice analysis."
                else:
                    return "Hi! I can detect deepfakes in images and synthetic voices in audio. Send a photo or audio file to get started."
            
            else:
                return "Send a photo or audio file for deepfake detection, or ask me about my capabilities."
                
        except Exception as e:
            return f"Sorry, an error occurred: {str(e)}"

    def detect_image(self, file_path: str):
        """Send image to backend for analysis"""
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path, f, 'image/jpeg')}
                response = requests.post(f"{BACKEND_URL}/detect-image", files=files)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {"error": f"Failed to analyze image: {str(e)}"}

    def detect_audio(self, file_path: str):
        """Send audio to backend for analysis"""
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path, f, 'audio/wav')}
                response = requests.post(f"{BACKEND_URL}/detect-audio", files=files)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {"error": f"Failed to analyze audio: {str(e)}"}

    def format_result(self, result):
        """Format analysis results for user-friendly display"""
        if "error" in result:
            return f"❌ {result['error']}"
        
        if result["type"] == "image":
            confidence_pct = int(result['confidence'] * 100)
            if result['result'] == 'deepfake':
                return f"🚨 This image appears to be a DEEPFAKE with {confidence_pct}% confidence.\n📝 {result['explanation']}"
            else:
                return f"✅ This image appears to be REAL with {confidence_pct}% confidence.\n📝 {result['explanation']}"
        
        elif result["type"] == "audio":
            confidence_pct = int(result['confidence'] * 100)
            if result['result'] == 'synthetic':
                return f"🚨 This voice appears to be SYNTHETIC with {confidence_pct}% confidence.\n📝 {result['explanation']}"
            else:
                return f"✅ This voice appears to be HUMAN with {confidence_pct}% confidence.\n📝 {result['explanation']}"
        
        return str(result)

def run_interactive_mode():
    """Run the agent in interactive mode for testing"""
    agent = DeepfakeDetectionAgent(name="deepfake_detector")
    
    print("🧾 Multimodal Deepfake Detection Agent")
    print("=" * 50)
    print("Commands:")
    print("- Type a message to chat")
    print("- Type 'test image' to test with a sample image")
    print("- Type 'test audio' to test with a sample audio") 
    print("- Type 'quit' to exit")
    print("=" * 50)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        elif user_input.lower() == 'test image':
            # Create a test image for demonstration
            from PIL import Image
            test_img = Image.new('RGB', (100, 100), color='blue')
            test_img.save('test_image.png')
            response = agent.process_message(file_path='test_image.png', file_type='image/png')
            print(f"Agent: {response}")
            import os
            os.remove('test_image.png')
        elif user_input.lower() == 'test audio':
            response = agent.process_message(message_text="I need an audio file to test")
            print(f"Agent: {response}")
        else:
            response = agent.process_message(message_text=user_input)
            print(f"Agent: {response}")

if __name__ == "__main__":
    run_interactive_mode()
