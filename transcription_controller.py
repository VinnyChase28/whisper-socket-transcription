import threading
from whisper_transcriber import WhisperTranscriber

class TranscriptionController:
    def __init__(self, socketio):
        self.transcriber = WhisperTranscriber(socketio)
        self.thread = None  # Keep track of the transcription thread

    def start_transcription(self, sid):  # Accept the SID parameter
        if not self.transcriber.running:
            # Pass the SID to the transcriber's start_transcription method
            self.thread = threading.Thread(target=self.transcriber.start_transcription, args=(sid,))
            self.thread.daemon = True
            self.thread.start()

    def stop_transcription(self, sid):  # Accept the SID parameter
        # Pass the SID to the transcriber's stop_transcription method, if it needs to emit messages
        self.transcriber.stop_transcription(sid)
        if self.thread is not None:
            self.thread.join()  # Wait for the transcription thread to finish
            self.thread = None  # Reset the thread reference