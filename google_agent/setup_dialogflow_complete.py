"""
Complete Dialogflow CX setup with webhook configuration
"""
from google.cloud import dialogflowcx_v3 as dialogflow
import json
import os

def create_complete_dialogflow_setup():
    """Create agent, webhook, and intents programmatically"""
    
    project_id = "project-jer-467014"
    location = "us-central1"
    webhook_url = "https://deepfake-detection-webhook-31255625957.us-central1.run.app/webhook"
    
    print("🤖 Creating complete Dialogflow CX setup...")
    
    try:
        # Initialize clients with regional endpoint
        client_options = {"api_endpoint": f"{location}-dialogflow.googleapis.com"}
        agents_client = dialogflow.AgentsClient(client_options=client_options)
        webhooks_client = dialogflow.WebhooksClient(client_options=client_options)
        intents_client = dialogflow.IntentsClient(client_options=client_options)
        
        # Create agent
        parent = f"projects/{project_id}/locations/{location}"
        
        agent = dialogflow.Agent(
            display_name="Deepfake Detection Agent",
            default_language_code="en",
            time_zone="America/New_York",
            description="Multimodal deepfake detection agent with image and audio analysis"
        )
        
        print("📝 Creating agent...")
        created_agent = agents_client.create_agent(parent=parent, agent=agent)
        agent_name = created_agent.name
        print(f"✅ Agent created: {agent_name}")
        
        # Create webhook
        webhook = dialogflow.Webhook(
            display_name="Deepfake Detection Webhook",
            generic_web_service=dialogflow.Webhook.GenericWebService(
                uri=webhook_url
            )
        )
        
        print("🔗 Creating webhook...")
        created_webhook = webhooks_client.create_webhook(
            parent=agent_name, webhook=webhook
        )
        webhook_name = created_webhook.name
        print(f"✅ Webhook created: {webhook_name}")
        
        # Create intents with webhook fulfillment
        intents_data = [
            {
                "display_name": "image.detection",
                "training_phrases": [
                    "Check this image",
                    "Is this photo fake?",
                    "Analyze this picture",
                    "Detect deepfake in image",
                    "Is this image real?",
                    "Photo analysis"
                ]
            },
            {
                "display_name": "audio.detection", 
                "training_phrases": [
                    "Check this voice",
                    "Is this audio real?",
                    "Analyze this sound",
                    "Detect voice cloning",
                    "Is this voice fake?",
                    "Audio analysis"
                ]
            },
            {
                "display_name": "general.help",
                "training_phrases": [
                    "What can you do?",
                    "Help me",
                    "How does this work?",
                    "What is deepfake detection?"
                ]
            }
        ]
        
        for intent_data in intents_data:
            intent = dialogflow.Intent(
                display_name=intent_data["display_name"],
                training_phrases=[
                    dialogflow.Intent.TrainingPhrase(
                        parts=[dialogflow.Intent.TrainingPhrase.Part(text=phrase)]
                    )
                    for phrase in intent_data["training_phrases"]
                ],
                fulfillment=dialogflow.Fulfillment(
                    webhook=webhook_name
                )
            )
            
            print(f"📋 Creating intent: {intent_data['display_name']}...")
            created_intent = intents_client.create_intent(
                parent=agent_name, intent=intent
            )
            print(f"✅ Intent created: {created_intent.name}")
        
        # Extract agent ID from the full name
        agent_id = created_agent.name.split('/')[-1]
        
        print("\n🎉 Complete setup successful!")
        print(f"🔗 Agent Console URL: https://dialogflow.cloud.google.com/cx/projects/{project_id}/locations/{location}/agents/{agent_id}")
        print(f"📝 Agent ID: {agent_id}")
        
        return {
            "agent_name": agent_name,
            "agent_id": agent_id,
            "webhook_name": webhook_name,
            "webhook_url": webhook_url,
            "console_url": f"https://dialogflow.cloud.google.com/cx/projects/{project_id}/locations/{location}/agents/{agent_id}"
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Tip: Make sure you have proper authentication credentials")
        print("   Run: gcloud auth application-default login")
        return None

def list_existing_agents():
    """List existing Dialogflow CX agents"""
    
    project_id = "project-jer-467014"
    location = "us-central1"
    
    try:
        client_options = {"api_endpoint": f"{location}-dialogflow.googleapis.com"}
        agents_client = dialogflow.AgentsClient(client_options=client_options)
        parent = f"projects/{project_id}/locations/{location}"
        
        print("🔍 Listing existing agents...")
        agents = agents_client.list_agents(parent=parent)
        
        agent_list = []
        for agent in agents:
            agent_id = agent.name.split('/')[-1]
            agent_info = {
                "name": agent.display_name,
                "id": agent_id,
                "full_name": agent.name,
                "console_url": f"https://dialogflow.cloud.google.com/cx/projects/{project_id}/locations/{location}/agents/{agent_id}"
            }
            agent_list.append(agent_info)
            print(f"📋 Agent: {agent.display_name} (ID: {agent_id})")
            print(f"   URL: {agent_info['console_url']}")
        
        return agent_list
        
    except Exception as e:
        print(f"❌ Error listing agents: {e}")
        return []

def setup_authentication():
    """Check and set up authentication"""
    
    print("🔐 Checking authentication...")
    
    # Check if we have default credentials
    try:
        from google.auth import default
        credentials, project = default()
        print(f"✅ Found credentials for project: {project}")
        return True
    except Exception as e:
        print(f"❌ Authentication issue: {e}")
        print("\n💡 To fix authentication, run:")
        print("   gcloud auth application-default login")
        print("   gcloud config set project project-jer-467014")
        return False

if __name__ == "__main__":
    print("🚀 Dialogflow CX Agent Setup")
    print("=" * 50)
    
    # Check authentication first
    if not setup_authentication():
        print("\n🔧 Please set up authentication and try again.")
        exit(1)
    
    # First, list existing agents
    existing_agents = list_existing_agents()
    
    if existing_agents:
        print(f"\n📊 Found {len(existing_agents)} existing agent(s)")
        print("Would you like to:")
        print("1. Use existing agent")
        print("2. Create new agent")
        try:
            choice = input("Enter choice (1 or 2): ").strip()
        except KeyboardInterrupt:
            print("\n👋 Setup cancelled.")
            exit(0)
        
        if choice == "1":
            print("✅ Using existing agent. Check the console URLs above.")
            exit(0)
    
    # Create new agent
    print("\n🏗️ Creating new agent...")
    result = create_complete_dialogflow_setup()
    
    if result:
        print("\n📋 Configuration Summary:")
        print(f"Agent: {result['agent_name']}")
        print(f"Agent ID: {result['agent_id']}")
        print(f"Webhook: {result['webhook_name']}")
        print(f"URL: {result['webhook_url']}")
        print(f"Console: {result['console_url']}")
        
        print("\n🎯 Next Steps:")
        print("1. Open the console URL above")
        print("2. Test the agent in the simulator")
        print("3. Add training phrases if needed")
        print("4. Deploy to web/phone/etc.")
        
        # Save configuration to file
        config_file = "dialogflow_config.json"
        with open(config_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Configuration saved to: {config_file}")
    
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
        print("🔧 Common solutions:")
        print("   1. Run: gcloud auth application-default login")
        print("   2. Enable Dialogflow CX API in your project")
        print("   3. Make sure you have proper permissions")
