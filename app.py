from flask import Flask, send_from_directory
from google.cloud import vision

app = Flask(__name__)
client = vision.ImageAnnotatorClient()


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/detect-text")
def route_detect_text():
    content = ""
    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    for text in texts:
        print('\n"{}"'.format(text.description))
    return ""


@app.route("/detect-scene")
def route_detect_scene():
    return ""


@app.route("/caption")
def route_caption():
    return ""


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
