import threading

class TranscriptionController:
    def __init__(self):
        self.transcriber = WhisperTranscriber()
        self.thread = None  # Keep track of the transcription thread

    def start_transcription(self):
        if not self.transcriber.running:
            # Start the transcription thread only if it's not already running
            self.thread = threading.Thread(target=self.transcriber.start_transcription)
            self.thread.daemon = True
            self.thread.start()

    def stop_transcription(self):
        self.transcriber.stop_transcription()  # Signal the transcriber to stop
        if self.thread is not None:
            self.thread.join()  # Wait for the transcription thread to finish
            self.thread = None  # Reset the thread reference
