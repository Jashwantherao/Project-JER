# Google Cloud deployment script for Dialogflow CX Deepfake Detection (PowerShell)

# Configuration
$PROJECT_ID = ""
$REGION = "us-central1"
$SERVICE_NAME = "deepfake-detection-webhook"
$IMAGE_NAME = "deepfake-detection"
$REPOSITORY_NAME = "deepfake-repo"

Write-Host "🚀 Deploying Deepfake Detection Agent to Google Cloud" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Check if gcloud is installed
try {
    $gcloudVersion = gcloud --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "gcloud not found"
    }
} catch {
    Write-Host "❌ Google Cloud CLI not found. Please install it first:" -ForegroundColor Red
    Write-Host "   https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    exit 1
}

# Set project
Write-Host "📋 Setting Google Cloud project: $PROJECT_ID" -ForegroundColor Cyan
gcloud config set project $PROJECT_ID

# Enable required APIs
Write-Host "🔧 Enabling required APIs..." -ForegroundColor Cyan
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com  
gcloud services enable dialogflow.googleapis.com
gcloud services enable artifactregistry.googleapis.com

# Create Artifact Registry repository (if it doesn't exist)
Write-Host "📦 Creating Artifact Registry repository..." -ForegroundColor Cyan
gcloud artifacts repositories create $REPOSITORY_NAME `
    --repository-format=docker `
    --location=$REGION `
    --description="Deepfake detection webhook images" `
    --quiet 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Repository already exists or error occurred" -ForegroundColor Yellow
}

# Configure Docker authentication
Write-Host "🔐 Configuring Docker authentication..." -ForegroundColor Cyan
gcloud auth configure-docker "${REGION}-docker.pkg.dev" --quiet

# Build container image using Artifact Registry
Write-Host "🏗️  Building container image..." -ForegroundColor Cyan
$imageUri = "${REGION}-docker.pkg.dev/$PROJECT_ID/$REPOSITORY_NAME/${IMAGE_NAME}:latest"
gcloud builds submit --tag $imageUri .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed. Check the error output above." -ForegroundColor Red
    exit 1
}

# Deploy to Cloud Run
Write-Host "🚀 Deploying to Cloud Run..." -ForegroundColor Cyan
gcloud run deploy $SERVICE_NAME `
    --image $imageUri `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --memory 4Gi `
    --cpu 2 `
    --timeout 300 `
    --max-instances 10 `
    --min-instances 0 `
    --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID,PORT=8080" `
    --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Deployment failed. Check the error output above." -ForegroundColor Red
    exit 1
}

# Get service URL
$SERVICE_URL = gcloud run services describe $SERVICE_NAME --region $REGION --format "value(status.url)"

Write-Host "✅ Deployment completed!" -ForegroundColor Green
Write-Host "📍 Service URL: $SERVICE_URL" -ForegroundColor Cyan
Write-Host "🔗 Webhook URL: $SERVICE_URL/webhook" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Copy the webhook URL: $SERVICE_URL/webhook" -ForegroundColor White
Write-Host "   2. Go to Dialogflow CX console" -ForegroundColor White
Write-Host "   3. Configure fulfillment with this webhook URL" -ForegroundColor White
Write-Host "   4. Test your agent!" -ForegroundColor White

# Test the deployment
Write-Host "🧪 Testing deployment..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri $SERVICE_URL -UseBasicParsing -TimeoutSec 30
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Health check passed" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Health check returned status: $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Health check failed: $($_.Exception.Message)" -ForegroundColor Yellow
}
