# 🎯 Dialogflow CX Manual Webhook Configuration

## ✅ Current Status
- **Webhook Created**: ✅ `projects/project-jer-467014/locations/us-central1/agents/1cefccb6-7f9e-44e8-bcd4-c741f68c1140/webhooks/ab8c869-d9eb-4dc4-b43c-6a576ae24be2`
- **Webhook URL**: `https://deepfake-detection-webhook-31255625957.us-central1.run.app/webhook`
- **Agent URL**: `https://dialogflow.cloud.google.com/cx/projects/project-jer-467014/locations/us-central1/agents/1cefccb6-7f9e-44e8-bcd4-c741f68c1140`

## 🔧 Manual Configuration Steps

### 1. Open Agent Console
Go to: [Dialogflow CX Agent Console](https://dialogflow.cloud.google.com/cx/projects/project-jer-467014/locations/us-central1/agents/1cefccb6-7f9e-44e8-bcd4-c741f68c1140)

### 2. Navigate to Build Section
- Click **"Build"** in the left sidebar
- You'll see **"Flows"**, **"Intents"**, **"Entity Types"**, etc.

### 3. Create Custom Intents
Click **"Intents"** → **"Create"** → **"New Intent"**

#### Intent 1: Image Detection
- **Display Name**: `deepfake.image.detection`
- **Training Phrases**:
  - "Check this image for deepfakes"
  - "Is this photo fake?"
  - "Analyze this picture"
  - "Detect deepfake in image"
  - "Is this image real?"
- **Fulfillment**: 
  - Toggle **"Enable webhook"**
  - **Tag**: `image-detection`
- Click **"Save"**

#### Intent 2: Audio Detection
- **Display Name**: `deepfake.audio.detection`
- **Training Phrases**:
  - "Check this voice"
  - "Is this audio real?"
  - "Analyze this sound"
  - "Detect voice cloning"
  - "Is this voice fake?"
- **Fulfillment**:
  - Toggle **"Enable webhook"**
  - **Tag**: `audio-detection`
- Click **"Save"**

#### Intent 3: Help
- **Display Name**: `deepfake.help`
- **Training Phrases**:
  - "What can you do?"
  - "How does deepfake detection work?"
  - "Help with deepfakes"
  - "What is deepfake detection?"
- **Fulfillment**:
  - Toggle **"Enable webhook"**
  - **Tag**: `help`
- Click **"Save"**

### 4. Configure Default Start Flow
- Go to **"Flows"** → **"Default Start Flow"**
- Click on **"Start"** page
- In the **"Fulfillment"** section:
  - Toggle **"Enable webhook"**
  - Select your webhook from dropdown
  - **Tag**: `welcome`

### 5. Test in Simulator
- Click **"Test Agent"** in the right panel
- Try these phrases:
  - "Check this image for deepfakes"
  - "Is this audio real?"
  - "What can you do?"

## 🧪 Test Commands

You can test the webhook responses directly:

```bash
# Test webhook directly
python test_webhook_direct.py

# Test agent integration
python test_agent_integration.py
```

## 🔗 Quick Links

- **Agent Console**: [Open Dialogflow CX](https://dialogflow.cloud.google.com/cx/projects/project-jer-467014/locations/us-central1/agents/1cefccb6-7f9e-44e8-bcd4-c741f68c1140)
- **Webhook URL**: `https://deepfake-detection-webhook-31255625957.us-central1.run.app/webhook`
- **Health Check**: `https://deepfake-detection-webhook-31255625957.us-central1.run.app/`

## 📋 Webhook Tags for Different Functions

When configuring fulfillment tags in the console:

| Intent Type | Tag | Purpose |
|------------|-----|---------|
| Image Detection | `image-detection` | Analyzes uploaded images |
| Audio Detection | `audio-detection` | Analyzes audio files |
| Help/Welcome | `help` | General assistance |
| Default Welcome | `welcome` | Initial greeting |

## ✅ Verification

After manual configuration, the agent should:
1. Respond with webhook-generated messages
2. Handle image/audio detection requests
3. Provide appropriate help responses

## 🎯 Integration Complete

Once manually configured, your Google ADK (Dialogflow CX) integration will be fully operational with:
- ✅ Cloud-deployed webhook service
- ✅ Dialogflow CX agent with custom intents
- ✅ Webhook fulfillment for deepfake detection
- ✅ Production-ready architecture
