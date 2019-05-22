import os
import sys

import cv2
from flask import Flask, send_from_directory
from google.cloud import vision

from scripts.scene_detection import *
from scripts.text_to_speech import *


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"

app = Flask(__name__)
client = vision.ImageAnnotatorClient()


@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/reset")
def reset():
    python = sys.executable
    os.execl(python, python, *sys.argv)

@app.route("/detect-text")
def route_detect_text():
    content = capture_frame()
    cv2.imwrite('image.png', content)
    image = cv2.imread('image.png')
    _, encoded_image = cv2.imencode('.png', image)
    content = encoded_image.tobytes()
    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    os.remove('image.png')
    print('Texts:')
    # for text in texts:
    #     print('\n"{}"'.format(text.description))
    try:
        sent = '\n{}'.format(texts[0].description)
        speech(sent)
        print(sent)
    except:
        pass
    return ""


@app.route("/detect-scene")
def route_detect_scene():
    scene,obj = scene_detect()
    speech(scene)
    if obj != None:
        speech(obj)
    return "scene: " + scene +" obj: " + str(obj)


@app.route("/caption")
def route_caption():
    return ""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
