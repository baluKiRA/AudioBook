from flask import Flask, request, jsonify, send_file
import requests
from config import BASE_URL  # The ngrok URL for the Colab backend
import os

app = Flask(__name__)

# Route to fetch the list of books
@app.route('/books', methods=['GET'])
def get_books():
    try:
        response = requests.get(f"{BASE_URL}/books")
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Failed to fetch books from backend'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to upload a file and process it
@app.route('/upload', methods=['POST'])
def upload_and_process():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        files = {'file': file}
        response = requests.post(f"{BASE_URL}/upload", files=files)
        if response.status_code == 200:
            return jsonify(response.json())  # Relay response to the React frontend
        else:
            return jsonify({'error': 'Failed to process file'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to fetch the audio file
@app.route('/audio', methods=['GET'])
def get_audio():
    try:
        response = requests.get(f"{BASE_URL}/audio", stream=True)
        if response.status_code == 200:
            # Save the audio locally (optional)
            audio_path = 'combined_audio.wav'
            with open(audio_path, 'wb') as audio_file:
                for chunk in response.iter_content(chunk_size=8192):
                    audio_file.write(chunk)
            return send_file(audio_path, mimetype="audio/wav")
        else:
            return jsonify({'error': 'Failed to fetch audio'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)  # Run the Python server on localhost:5000
