import os
import win32com.client as wincl

# class TextToSpeech:

def speech(text):
  speak = wincl.Dispatch('SAPI.SpVoice')
  speak.Speak(text)
        # os.system("espeak -v ta '%s'" % text)

# if __name__ == "__main__":
#   speech('sumit')