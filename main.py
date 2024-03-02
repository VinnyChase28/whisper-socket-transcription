from flask import Flask, jsonify
import threading
from whisper_transcriber import WhisperTranscriber  # Import the class

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    transcriber = WhisperTranscriber()  # Instantiate the class
    thread = threading.Thread(target=transcriber.start_transcription)
    thread.daemon = True
    thread.start()
    
    return jsonify({"message": "Transcription started"}), 200

if __name__ == '__main__':
    app.run(debug=True)