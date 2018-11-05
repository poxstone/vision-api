import io, os, sys
import logging

from flask import Flask
from google.cloud import vision
from google.cloud.vision import types
from google.auth import compute_engine


app = Flask(__name__)


def getAppengine():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
        sys.path[0] + "/credential.json"

    credentials = compute_engine.Credentials()
    return credentials


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    credentials = getAppengine()

    client = vision.ImageAnnotatorClient()
    logging.info(credentials)

    file_name = os.path.join(os.path.dirname(__file__), 'resources/tomaco.jpg')
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    for label in labels:
        print(label.description)

    return str(label)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

