import pyaudio
import wave
import threading
import keyboard
import whisper
import pyautogui
import argparse
from queue import Queue
    
class AudioRecorder:
    def __init__(self, chunk=1024, sample_format=pyaudio.paInt16, channels=1, fs=44100, filename="output.wav", language='中文',  hotkey='alt+x', callback=None):
        self.chunk = chunk
        self.sample_format = sample_format
        self.channels = channels
        self.fs = fs
        self.filename = filename
        self.callback = callback
        self.frames = []
        self.recording = False
        self.new_recording = threading.Event()
        self.hotkey = hotkey
        self.model = whisper.load_model("medium")
        self.language = language
        self.transcription_queue = Queue()
        self.p = pyaudio.PyAudio()

    def toggle_recording(self):
        self.recording = not self.recording
        if self.recording:
            print('Recording')
            self.frames = []  # Clear previous recording frames
            threading.Thread(target=self.record).start()
        else:
            print('Stopped recording')

    def record(self):
        stream = self.p.open(
            format=self.sample_format,
            channels=self.channels,
            rate=self.fs,
            frames_per_buffer=self.chunk,
            input=True
        )
        while self.recording:
            data = stream.read(self.chunk)
            self.frames.append(data)
        stream.stop_stream()
        stream.close()
        self.save_audio()

    def transcribe_recording(self):
        options = {
        "language": self.language, 
        "task": "transcribe"
        }
        result = self.model.transcribe(self.filename, **options)
        return result["text"]

    def save_audio(self):
        # Save the recorded audio to a file
        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.sample_format))
            wf.setframerate(self.fs)
            wf.writeframes(b''.join(self.frames))
        
        # Transcribe the audio file
        transcription = self.transcribe_recording()

        # Use the queue to pass the transcription back to the main thread
        self.transcription_queue.put(transcription)
        
        # Signal that a new recording is available
        self.new_recording.set()  

        # If you still need to use a callback for other purposes, you can, but ensure it's deliberate
        if self.callback:
            self.callback(transcription)


    def start_hotkey_listener(self):
        # This function will start the hotkey listener in a new thread.
        listener_thread = threading.Thread(target=self.listen_for_hotkey)
        listener_thread.daemon = True
        listener_thread.start()

    def listen_for_hotkey(self):
        # Use the instance's hotkey variable instead of passing it as an argument
        keyboard.add_hotkey(self.hotkey, self.toggle_recording, suppress=True)
        keyboard.wait('esc')
    
    def set_language(self, language):
        self.language = language
        print("The language is currently set to: ", self.language)


def main():
    parser = argparse.ArgumentParser(description='Audio Recorder and Transcriber')
    parser.add_argument('--hotkey', type=str, default='alt+x', help='Hotkey to toggle recording')
    parser.add_argument('--language', type=str, default='en', help='Language for transcription')
    args = parser.parse_args()

    recorder = AudioRecorder()
    recorder.set_language(args.language)
    recorder.listen_for_hotkey(args.hotkey)
    


if __name__ == "__main__":
    main()
