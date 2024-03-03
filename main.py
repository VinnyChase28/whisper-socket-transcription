from flask import Flask
from flask_socketio import SocketIO, emit
from transcription_controller import TranscriptionController

app = Flask(__name__)
socketio = SocketIO(app)

transcription_controller = TranscriptionController()

@socketio.on('start_transcription')
def handle_start_transcription():
    transcription_controller.start_transcription()
    emit('status', {'message': 'Transcription started'})

@socketio.on('stop_transcription')
def handle_stop_transcription():
    transcription_controller.stop_transcription()
    emit('status', {'message': 'Transcription stopped'})

if __name__ == '__main__':
    socketio.run(app, debug=True)