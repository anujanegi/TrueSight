import os

class TextToSpeech:

    def speech(text):
        os.system("espeak -v ta '%s'" % text)
