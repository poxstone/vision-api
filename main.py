import os

from flask import Flask

from app_vision.helpers import VisionHelper
from app_vision.constants import BUCKET, CREDENTIAL_JSON, ROOT_PATH


# For local debug
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ROOT_PATH + '/' + CREDENTIAL_JSON

# Run flask
app = Flask(__name__)


@app.route('/')
def hello():

    bucket_img = BUCKET + '/images/tomaco_man.jpg'
    img_local = ROOT_PATH + '/resources/tomaco_man.jpg'

    # Init Api
    visionApi = VisionHelper()
    response_color = visionApi.getImageProperties(img_local)
    response_labels = visionApi.getLocalLabels(img_local)
    response_face = visionApi.getFace(bucket_img)

    # Response
    return 'Response [{}] \n\n [{}] \n\n [{}]'.format(
        str(response_color), str(response_labels), str(response_face))


# Run app
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

