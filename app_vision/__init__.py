import logging
import json
import config

from flask import Flask
from flask.templating import render_template

from app_vision.helpers import VisionHelper
from app_vision.constants import BUCKET


# Run flask

def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)

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

   

    return app
     
