import json
from vosk import Model, KaldiRecognizer
from config import SAMPLE_RATE, KO_MODEL_PATH, EN_MODEL_PATH

class DualRecognizer:
    def __init__(self):
        self.ko_model = Model(KO_MODEL_PATH)
        self.en_model = Model(EN_MODEL_PATH)
        self.ko_recognizer = KaldiRecognizer(self.ko_model, SAMPLE_RATE)
        self.en_recognizer = KaldiRecognizer(self.en_model, SAMPLE_RATE)

    def recognize(self, data):
        ko_text = ""
        en_text = ""

        if self.ko_recognizer.AcceptWaveform(data):
            result = json.loads(self.ko_recognizer.Result())
            ko_text = result.get("text", "")
        if self.en_recognizer.AcceptWaveform(data):
            result = json.loads(self.en_recognizer.Result())
            en_text = result.get("text", "")

        return ko_text, en_text

class SingleRecognizer:
    def __init__(self, lang):
        if lang == 'ko':
            self.model = Model(KO_MODEL_PATH)
        else:
            self.model = Model(EN_MODEL_PATH)
            
        self.recognizer = KaldiRecognizer(self.model, SAMPLE_RATE)

    def recognize(self, data):
        if self.recognizer.AcceptWaveform(data):
            return self.recognizer.Result()
        return None
