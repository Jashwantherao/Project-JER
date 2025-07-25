"""
Standalone Google ADK (Dialogflow CX) Terminal Interface
Run the deepfake detection agent directly from command line
"""
import requests
import json
import os
import base64
from datetime import datetime

class DialogflowTerminalAgent:
    def __init__(self):
        self.webhook_url = "https://deepfake-detection-webhook-31255625957.us-central1.run.app"
        self.session_id = f"terminal-session-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.conversation_history = []
        
    def send_message(self, message, file_path=None):
        """Send message to the agent"""
        
        payload = {
            "message": message,
            "session_id": self.session_id
        }
        
        # Handle file upload
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    file_content = base64.b64encode(f.read()).decode()
                
                file_ext = os.path.splitext(file_path)[1].lower()
                if file_ext in ['.jpg', '.jpeg', '.png']:
                    payload['image_data'] = file_content
                    payload['image_filename'] = os.path.basename(file_path)
                elif file_ext in ['.wav', '.mp3', '.flac']:
                    payload['audio_data'] = file_content
                    payload['audio_filename'] = os.path.basename(file_path)
                    
                print(f"📎 Attached file: {os.path.basename(file_path)}")
            except Exception as e:
                print(f"❌ Error reading file: {e}")
                return None
        
        try:
            response = requests.post(
                f"{self.webhook_url}/chat",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                self.conversation_history.append({
                    "user": message,
                    "agent": result.get("response", "No response"),
                    "intent": result.get("intent", "unknown"),
                    "confidence": result.get("confidence", 0.0)
                })
                return result
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return None
    
    def detect_file(self, file_path):
        """Direct file detection without conversation"""
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return None
            
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f)}
                
                response = requests.post(
                    f"{self.webhook_url}/detect-file",
                    files=files,
                    timeout=60
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"❌ Detection error: {response.status_code}")
                    return None
                    
        except Exception as e:
            print(f"❌ File detection error: {e}")
            return None
    
    def show_conversation_history(self):
        """Display conversation history"""
        
        if not self.conversation_history:
            print("📝 No conversation history yet.")
            return
            
        print("\n📋 Conversation History:")
        print("=" * 50)
        
        for i, exchange in enumerate(self.conversation_history, 1):
            print(f"\n{i}️⃣ User: {exchange['user']}")
            print(f"🤖 Agent: {exchange['agent']}")
            print(f"   📊 Intent: {exchange['intent']} (confidence: {exchange['confidence']:.2f})")
    
    def run_interactive_mode(self):
        """Run interactive terminal mode"""
        
        print("🤖 Google ADK Deepfake Detection Agent")
        print("=" * 45)
        print("Commands:")
        print("  • Type messages to chat with the agent")
        print("  • 'upload <filepath>' - Analyze a file")
        print("  • 'detect <filepath>' - Direct file detection")
        print("  • 'history' - Show conversation history")
        print("  • 'quit' - Exit")
        print("=" * 45)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                    
                elif user_input.lower() == 'history':
                    self.show_conversation_history()
                    continue
                    
                elif user_input.lower().startswith('upload '):
                    file_path = user_input[7:].strip()
                    result = self.send_message("Analyze this file", file_path)
                    
                elif user_input.lower().startswith('detect '):
                    file_path = user_input[7:].strip()
                    print(f"🔍 Analyzing file: {file_path}")
                    result = self.detect_file(file_path)
                    
                    if result:
                        print(f"🤖 Detection Result:")
                        print(f"   📊 Type: {result.get('detection_type', 'unknown')}")
                        print(f"   📈 Confidence: {result.get('confidence', 0):.1%}")
                        print(f"   💭 Explanation: {result.get('explanation', 'N/A')}")
                    continue
                    
                else:
                    result = self.send_message(user_input)
                
                if result:
                    print(f"🤖 Agent: {result.get('response', 'No response')}")
                    if 'intent' in result:
                        print(f"   📊 Intent: {result['intent']} (confidence: {result.get('confidence', 0):.2f})")
                        
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Main function for terminal interface"""
    
    import sys
    
    agent = DialogflowTerminalAgent()
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'test':
            # Quick test mode
            print("🧪 Testing Google ADK Integration...")
            result = agent.send_message("Hello! What can you help me with?")
            if result:
                print(f"✅ Agent responded: {result.get('response', 'No response')}")
            else:
                print("❌ Agent test failed")
                
        elif command == 'detect' and len(sys.argv) > 2:
            # Direct file detection
            file_path = sys.argv[2]
            print(f"🔍 Detecting file: {file_path}")
            result = agent.detect_file(file_path)
            
            if result:
                print(f"📊 Detection: {result.get('detection_type', 'unknown')}")
                print(f"📈 Confidence: {result.get('confidence', 0):.1%}")
                print(f"💭 Explanation: {result.get('explanation', 'N/A')}")
            else:
                print("❌ Detection failed")
                
        elif command == 'chat':
            # Direct chat mode
            if len(sys.argv) > 2:
                message = ' '.join(sys.argv[2:])
                result = agent.send_message(message)
                if result:
                    print(result.get('response', 'No response'))
            else:
                print("Usage: python adk_terminal.py chat <message>")
                
        else:
            print("Usage:")
            print("  python adk_terminal.py test")
            print("  python adk_terminal.py detect <filepath>")
            print("  python adk_terminal.py chat <message>")
            print("  python adk_terminal.py  (interactive mode)")
    else:
        # Interactive mode
        agent.run_interactive_mode()

if __name__ == "__main__":
    main()
