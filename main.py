import os
import json

from flask import Flask
from flask.templating import render_template
from app_vision.helpers import VisionHelper
from app_vision.constants import BUCKET, CREDENTIAL_JSON, ROOT_PATH


# For local debug
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ROOT_PATH + '/' + CREDENTIAL_JSON

# Run flask
app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    return render_template('index.html')


@app.route('/get-image/<image_name>')
def getImage(image_name):
    img_bucket = BUCKET + '/' + image_name

    # Init Api
    visionApi = VisionHelper()
    response_color = visionApi.getImageProperties(img_bucket)
    response_labels = visionApi.getLocalLabels(img_bucket)

    response_json = {
        'color': response_color,
        'labels': response_labels
    }

    # Response
    return json.dumps(response_json, 'utf8')


# Run app
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

