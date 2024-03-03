import argparse
import os
import numpy as np
import speech_recognition as sr
import whisper
import torch
from flask_socketio import emit
from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform

class WhisperTranscriber:
    def __init__(self, model='medium', non_english=False, energy_threshold=1000, record_timeout=2, phrase_timeout=0.1, default_microphone=None):
        self.model_name = model
        self.non_english = non_english
        self.energy_threshold = energy_threshold
        self.record_timeout = record_timeout
        self.phrase_timeout = phrase_timeout
        self.default_microphone = default_microphone
        self.data_queue = Queue()
        self.transcription = ['']
        self.phrase_time = None
        self.initialize_model()
        self.initialize_recorder()
        self.running = False

    def initialize_model(self):
        model = self.model_name
        if self.model_name != "large" and not self.non_english:
            model = model + ".en"
        self.audio_model = whisper.load_model(model, device="cuda")

    def initialize_recorder(self):
        self.recorder = sr.Recognizer()
        self.recorder.energy_threshold = self.energy_threshold
        self.recorder.dynamic_energy_threshold = False

        if 'linux' in platform and self.default_microphone:
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                if self.default_microphone in name:
                    mic_index = 16  # Replace 16 with the correct index if different
                    self.source = sr.Microphone(sample_rate=16000, device_index=mic_index)
                    break
        else:
            self.source = sr.Microphone(sample_rate=16000)

    def record_callback(self, recognizer, audio):
        data = audio.get_raw_data()
        self.data_queue.put(data)

    def start_transcription(self):
        self.running = True  # Enable the transcription loop
        with self.source:
            self.recorder.adjust_for_ambient_noise(self.source)
        self.recorder.listen_in_background(self.source, self.record_callback, phrase_time_limit=self.record_timeout)

        while self.running:
            try:
                now = datetime.utcnow()
                if not self.data_queue.empty():
                    phrase_complete = False
                    if self.phrase_time and now - self.phrase_time > timedelta(seconds=self.phrase_timeout):
                        phrase_complete = True
                    self.phrase_time = now

                    audio_data = b''.join(self.data_queue.queue)
                    self.data_queue.queue.clear()

                    audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
                    result = self.audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
                    text = result['text'].strip()

                    if phrase_complete:
                        self.transcription.append(text)
                    else:
                        self.transcription[-1] = text

                    os.system('cls' if os.name=='nt' else 'clear')
                    for line in self.transcription:
                        emit('transcription_update', {'text': text})
                    print('', end='', flush=True)

                    sleep(0.1)
            except KeyboardInterrupt:
                break

        print("\n\nTranscription:")
        for line in self.transcription:
            emit('transcription_update', {'line': line})
            

