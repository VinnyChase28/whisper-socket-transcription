from flask import Flask, request
from flask_socketio import SocketIO, emit
from transcription_controller import TranscriptionController
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

transcription_controller = TranscriptionController(socketio)

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('start_transcription')
def handle_start_transcription():
    print('start_transcription event received')
    sid = request.sid  # Get the current session ID
    transcription_controller.start_transcription(sid)  # Pass SID to your method
    emit('status', {'message': 'Transcription started'})

@socketio.on('stop_transcription')
def handle_stop_transcription():
    sid = request.sid  # Get the current session ID
    transcription_controller.stop_transcription(sid)  # Pass SID to your method
    emit('status', {'message': 'Transcription stopped'})

# clear the transcription
@socketio.on('clear_transcription')
def handle_clear_transcription():
    transcription_controller.clear_transcription()
    emit('status', {'message': 'Transcription cleared'})

if __name__ == '__main__':
    socketio.run(app, debug=True)
