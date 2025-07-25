#!/bin/bash
# Google Cloud deployment script for Dialogflow CX Deepfake Detection

set -e

# Configuration
PROJECT_ID="project-jer-467014"
REGION="us-central1"
SERVICE_NAME="deepfake-detection-webhook"
IMAGE_NAME="deepfake-detection"
REPOSITORY_NAME="deepfake-repo"

echo "🚀 Deploying Deepfake Detection Agent to Google Cloud"
echo "=================================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud CLI not found. Please install it first:"
    echo "   https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Set project
echo "📋 Setting Google Cloud project: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable dialogflow.googleapis.com
gcloud services enable artifactregistry.googleapis.com

# Create Artifact Registry repository (if it doesn't exist)
echo "📦 Creating Artifact Registry repository..."
gcloud artifacts repositories create $REPOSITORY_NAME \
    --repository-format=docker \
    --location=$REGION \
    --description="Deepfake detection webhook images" \
    --quiet || echo "Repository already exists"

# Configure Docker authentication
echo "🔐 Configuring Docker authentication..."
gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet

# Build container image using Artifact Registry
echo "🏗️  Building container image..."
gcloud builds submit --tag ${REGION}-docker.pkg.dev/$PROJECT_ID/$REPOSITORY_NAME/$IMAGE_NAME:latest .

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image ${REGION}-docker.pkg.dev/$PROJECT_ID/$REPOSITORY_NAME/$IMAGE_NAME:latest \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 4Gi \
    --cpu 2 \
    --timeout 300 \
    --max-instances 10 \
    --min-instances 0 \
    --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID,PORT=8080" \
    --quiet

# Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')

echo "✅ Deployment completed!"
echo "📍 Service URL: $SERVICE_URL"
echo "🔗 Webhook URL: $SERVICE_URL/webhook"
echo ""
echo "📋 Next steps:"
echo "   1. Copy the webhook URL: $SERVICE_URL/webhook"
echo "   2. Go to Dialogflow CX console"
echo "   3. Configure fulfillment with this webhook URL"
echo "   4. Test your agent!"

# Test the deployment
echo "🧪 Testing deployment..."
curl -f "$SERVICE_URL/" && echo "✅ Health check passed"
