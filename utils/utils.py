from openai import OpenAI
import os
import speech_recognition as sr
from data import dbcreate
import sqlite3
from PySide6.QtCore import QObject, Signal

# Class that handles the voice input and voice to text functionality 
class VoiceListener(QObject):
    textChanged = Signal(str)
    text = ""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize db object
        self.db = dbcreate.Database("interview_manager.db")

        self.continue_listening = True  # Flag to control listening loop
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(device_index=self.db.get_device_id())

        self.OPEN_AI_TOKEN = self.db.get_ai_key()

        self.client = OpenAI(
          api_key=self.OPEN_AI_TOKEN,  # this is also the default, it can be omitted
        )

    def stop_listening(self):
        self.continue_listening = False  # Set flag to stop listening

    # Listens to the audio until the user stops
    def voice_to_text(self):
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            while self.continue_listening:
                try:
                    audio_chunk = self.recognizer.listen(source, timeout=5)
                    text = self.process_audio_chunk(audio_chunk)
                    if text:
                        self.text += text + " "
                        self.textChanged.emit(self.text)
                except KeyboardInterrupt:
                    print("Stopped listening.")
                    break
                except sr.WaitTimeoutError:
                    self.textChanged.emit("NA")
                    print("Timeout occurred while waiting for speech to start.")
                    break

    # Processes the audio into text 
    def process_audio_chunk(self, audio_chunk):
        text = ""
        try:
            text = self.recognizer.recognize_google(audio_chunk)
            print("You said:", text)
        except sr.UnknownValueError:
            self.textChanged.emit("NA")
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            self.textChanged.emit("NA")
            print("Error fetching results; {0}".format(e))
        return text

    # Gets the answer to the Voice to Text question.
    def get_ai_response(self, text):

        front_text = "In a point form response, please answer the following question: "

        # Send the message to OpenAI for processing
        response = self.client.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=front_text + text,
                max_tokens=500
            )
        answer = response.choices[0].text.strip()

        return answer

def find_devices():
    # Gives me a list of microphone sources
    devices = ""
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        devices = devices + "\"{1}\" `(device_index={0})`".format(index, name) + "\n"

    return devices