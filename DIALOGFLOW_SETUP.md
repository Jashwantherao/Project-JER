# Google Dialogflow CX Setup Guide

This guide walks you through setting up a production Dialogflow CX agent for the Deepfake Detection system.

## Prerequisites

1. **Google Cloud Project**
   - Create a new project or use existing one
   - Enable billing on the project

2. **Required APIs**
   ```bash
   gcloud services enable dialogflow.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   ```

## Step 1: Create Dialogflow CX Agent

1. **Go to Dialogflow CX Console**
   - Visit: https://dialogflow.cloud.google.com/cx/
   - Select your Google Cloud project

2. **Create New Agent**
   - Click "Create Agent"
   - Name: "Deepfake Detection Agent"
   - Location: "global" (or your preferred region)
   - Time zone: Your timezone
   - Language: "English"

3. **Note Agent Details**
   - Copy the Agent ID from the URL
   - Format: `projects/PROJECT_ID/locations/LOCATION/agents/AGENT_ID`

## Step 2: Configure Intents and Entities

### Default Welcome Intent
```
Training Phrases:
- "Hello"
- "Hi there"
- "What can you do?"
- "Help me detect deepfakes"

Response:
"Hello! I'm your deepfake detection assistant. I can analyze images for AI-generated content and audio files for synthetic voices. How can I help you today?"
```

### Detect Image Intent
```
Training Phrases:
- "Analyze this image"
- "Check if this photo is fake"
- "Is this image a deepfake?"
- "Detect deepfake in image"

Response:
"Please upload an image file and I'll analyze it for signs of AI generation."
```

### Detect Audio Intent
```
Training Phrases:
- "Check this voice recording"
- "Is this voice synthetic?"
- "Analyze this audio"
- "Detect voice cloning"

Response:
"Please upload an audio file and I'll analyze it for signs of voice synthesis."
```

### File Analysis Intent (Webhook)
```
Training Phrases:
- "Here's a file to analyze"
- "Check this file"

Parameters:
- file-path: @sys.any
- file-type: @sys.any

Fulfillment: Enable webhook
```

## Step 3: Deploy Webhook to Cloud Run

1. **Update Configuration**
   ```bash
   # Edit deploy.sh with your project details
   PROJECT_ID="your-actual-project-id"
   REGION="us-central1"  # or your preferred region
   ```

2. **Deploy to Cloud Run**
   ```bash
   # Make script executable (Linux/Mac)
   chmod +x deploy.sh
   
   # Run deployment
   ./deploy.sh
   ```

3. **Note Webhook URL**
   - Copy the Cloud Run service URL
   - Webhook endpoint: `https://YOUR-SERVICE-URL/webhook`

## Step 4: Configure Webhook in Dialogflow

1. **Go to Agent Settings**
   - In Dialogflow CX console, click "Manage" → "Webhooks"

2. **Create New Webhook**
   - Display Name: "Deepfake Detection Webhook"
   - Webhook URL: `https://YOUR-CLOUD-RUN-URL/webhook`
   - HTTP Method: POST
   - Timeout: 30 seconds

3. **Configure Fulfillment**
   - Go to each intent that needs webhook
   - In "Fulfillment" section, select your webhook
   - Enable "Use webhook" option

## Step 5: Test Your Agent

1. **Use Simulator**
   - In Dialogflow CX console, go to "Test Agent"
   - Try various conversation flows:
     - "Hello" → Should get welcome message
     - "Analyze image" → Should prompt for file upload
     - Upload test image → Should get analysis result

2. **Test Webhook Directly**
   ```bash
   # Test health check
   curl https://YOUR-CLOUD-RUN-URL/
   
   # Test chat endpoint
   curl -X POST https://YOUR-CLOUD-RUN-URL/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Hello", "session_id": "test"}'
   ```

## Step 6: Production Configuration

1. **Environment Variables**
   ```bash
   # Set in Cloud Run service
   GOOGLE_CLOUD_PROJECT=your-project-id
   DIALOGFLOW_LOCATION=global
   DIALOGFLOW_AGENT_ID=your-agent-id
   BACKEND_URL=https://your-backend-url  # If separate service
   ```

2. **Service Account (Optional)**
   ```bash
   # Create service account for webhook
   gcloud iam service-accounts create dialogflow-webhook
   
   # Grant Dialogflow permissions
   gcloud projects add-iam-policy-binding PROJECT_ID \
     --member="serviceAccount:dialogflow-webhook@PROJECT_ID.iam.gserviceaccount.com" \
     --role="roles/dialogflow.reader"
   ```

3. **Enable Authentication (Optional)**
   ```bash
   # For private webhook (requires authentication)
   gcloud run services add-iam-policy-binding deepfake-detection-webhook \
     --region=us-central1 \
     --member="serviceAccount:service-PROJECT_NUMBER@gcp-sa-dialogflow.iam.gserviceaccount.com" \
     --role="roles/run.invoker"
   ```

## Step 7: Integration Options

### Web Integration
```html
<!-- Add to your website -->
<script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>
<df-messenger
  intent="WELCOME"
  chat-title="Deepfake Detection Assistant"
  agent-id="YOUR_AGENT_ID"
  language-code="en">
</df-messenger>
```

### REST API Integration
```python
# Direct API calls to your webhook
import requests

response = requests.post('https://YOUR-CLOUD-RUN-URL/chat', json={
    'message': 'Hello, can you help me detect deepfakes?',
    'session_id': 'user123'
})
print(response.json())
```

### Mobile App Integration
Use the Dialogflow CX client libraries for iOS/Android to integrate directly with your agent.

## Troubleshooting

### Common Issues

1. **Webhook Timeout**
   - Increase timeout in Dialogflow webhook settings
   - Optimize model loading in backend

2. **Authentication Errors**
   - Verify service account permissions
   - Check Cloud Run IAM settings

3. **Model Loading Issues**
   - Increase Cloud Run memory allocation
   - Use pre-loaded model containers

### Monitoring and Logs

```bash
# View Cloud Run logs
gcloud logs read --service=deepfake-detection-webhook

# View Dialogflow logs in Cloud Console
# Go to: Cloud Logging > Logs Explorer
# Filter by: resource.type="dialogflow_agent"
```

## Cost Optimization

1. **Cloud Run Scaling**
   - Set minimum instances to 0 for cost savings
   - Configure CPU allocation based on usage

2. **Dialogflow Pricing**
   - First 1000 sessions per month are free
   - Monitor usage in Cloud Console billing

3. **Storage Optimization**
   - Use temporary file storage for uploads
   - Clean up files after processing

## Security Best Practices

1. **Input Validation**
   - Validate file types and sizes
   - Sanitize user inputs

2. **Rate Limiting**
   - Implement request rate limiting
   - Monitor for abuse patterns

3. **Data Privacy**
   - Don't store uploaded files permanently
   - Follow GDPR/privacy regulations

---

🎉 **Congratulations!** Your Dialogflow CX Deepfake Detection Agent is now ready for production use!
