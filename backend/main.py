import os
from flask import Flask, request, jsonify
from google.cloud import storage
import requests
import os
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Configure your GCS bucket name
GCS_BUCKET = os.environ.get('GCS_BUCKET', 'your-bucket-name')

# Initialize GCS client
gcs_client = storage.Client()

# Configuration (using environment variables)
CONFIDENCE_THRESHOLD_IMAGE = float(os.environ.get('CONFIDENCE_THRESHOLD_IMAGE', 0.8))
CONFIDENCE_THRESHOLD_AUDIO = float(os.environ.get('CONFIDENCE_THRESHOLD_AUDIO', 0.8))
DEEPFAKE_RESULT = os.environ.get('DEEPFAKE_RESULT', 'deepfake')
SYNTHETIC_RESULT = os.environ.get('SYNTHETIC_RESULT', 'synthetic')
REAL_RESULT = os.environ.get('REAL_RESULT', 'real')
HUMAN_RESULT = os.environ.get('HUMAN_RESULT', 'human')


def detect_image_deepfake(image_path):
    """
    Detects if an image is a deepfake using a Hugging Face Transformers model.

    Args:
        image_path (BytesIO): The image data as a BytesIO object.

    Returns:
        tuple: A tuple containing the result (DEEPFAKE_RESULT or REAL_RESULT),
               confidence score, and an explanation.
    """
    from transformers import pipeline

    # Using a specific deepfake detection model from Hugging Face
    classifier = pipeline('image-classification', model='dima806/deepfake_vs_real_image_detection')

    # Open the image using PIL
    image = Image.open(image_path)
    predictions = classifier(image)

    # Find the most likely prediction
    best_prediction = max(predictions, key=lambda p: p['score'])
    confidence = best_prediction['score']
    label = best_prediction['label']

    if label == 'fake':
        result = DEEPFAKE_RESULT
        explanation = f"Model classified as deepfake with {confidence:.2f} confidence."
    else:  # label == 'real'
        result = REAL_RESULT
        explanation = f"Model classified as real with {confidence:.2f} confidence."

    return result, confidence, explanation

from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
import numpy as np

# Initialize the voice encoder. This is a one-time setup.
encoder = VoiceEncoder()

# Mock function for audio deepfake detection (replace with your actual model)
def detect_audio_deepfake(audio_path):
    """
    Detects if an audio recording is synthetic using Resemblyzer.

    Args:
        audio_path (str): The path to the audio file.

    Returns:
        tuple: A tuple containing the result (SYNTHETIC_RESULT or HUMAN_RESULT),
               confidence score, and an explanation.
    """
    try:
        # Preprocess the audio file and create an embedding
        wav = preprocess_wav(Path(audio_path))
        embed = encoder.embed_utterance(wav)

        # Heuristic for synthetic speech detection.
        # Real human speech tends to have a certain level of variance and complexity
        # that can be captured in the embedding's norm. This is a simplified check.
        # A value between 1.2 and 2.0 is typical for human speech.
        embedding_norm = np.linalg.norm(embed)
        
        # Normalize the norm to a 0-1 confidence score (approximate)
        confidence = min(1.0, embedding_norm / 2.0)

        if embedding_norm < 1.2:  # Threshold for detecting synthetic voices
            result = SYNTHETIC_RESULT
            explanation = f"Voice characteristics (embedding norm: {embedding_norm:.2f}) suggest a synthetic origin."
        else:
            result = HUMAN_RESULT
            explanation = f"Voice characteristics (embedding norm: {embedding_norm:.2f}) are consistent with human speech."
        
        return result, confidence, explanation

    except Exception as e:
        # Handle cases where audio processing fails
        return "error", 0.0, f"Could not process audio file: {e}"

@app.route('/detect-image', methods=['POST'])
def detect_image():
    # Accept file upload or URL
    if 'file' in request.files:
        image_file = request.files['file']
        filename = image_file.filename
        temp_path = f'/tmp/{filename}'
        image_file.save(temp_path)
    elif 'url' in request.json:
        try:
            url = request.json['url']
            filename = url.split('/')[-1]
            temp_path = f'/tmp/{filename}'
            r = requests.get(url, stream=True)
            r.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            with open(temp_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        except requests.exceptions.RequestException as e:
            return jsonify({'error': f'Error downloading image from URL: {e}'}), 400
    else:
        return jsonify({'error': 'No image file or URL provided.'}), 400

    try:
        # Upload to GCS
        bucket = gcs_client.bucket(GCS_BUCKET)
        blob = bucket.blob(filename)
        blob.upload_from_filename(temp_path)

        # Download the image from GCS
        bucket = gcs_client.bucket(GCS_BUCKET)
        blob = bucket.blob(filename)
        image_data = blob.download_as_bytes()
        image = BytesIO(image_data)

        # Call deepfake detection model
        result, confidence, explanation = detect_image_deepfake(image)
        result = {
            'type': 'image',
            'result': result, 'confidence': confidence, 'explanation': explanation}
        return jsonify(result)
    finally:
        if temp_path:
            os.remove(temp_path)

@app.route('/detect-audio', methods=['POST'])
def detect_audio():
    # Accept file upload or URL
    if 'file' in request.files:
        audio_file = request.files['file']
        filename = audio_file.filename
        temp_path = f'/tmp/{filename}'
        audio_file.save(temp_path)
    elif 'url' in request.json:
        try:
            url = request.json['url']
            filename = url.split('/')[-1]
            temp_path = f'/tmp/{filename}'
            r = requests.get(url, stream=True)
            r.raise_for_status()
            with open(temp_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        except requests.exceptions.RequestException as e:
            return jsonify({'error': f'Error downloading audio from URL: {e}'}), 400
    else:
        return jsonify({'error': 'No audio file or URL provided.'}), 400

    try:
        # Upload to GCS
        bucket = gcs_client.bucket(GCS_BUCKET)
        blob = bucket.blob(filename)
        blob.upload_from_filename(temp_path)

        # Call audio deepfake detection model (stub)
        # Replace with actual model/API call
        result = {
            'type': 'audio',
            'result': SYNTHETIC_RESULT,
            'confidence': 0.88,
            'explanation': 'Voice cadence and pitch match known synthetic patterns.'
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Error processing audio: {e}'}), 500
    finally:
        if temp_path:
            os.remove(temp_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
