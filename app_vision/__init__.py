import logging
import json

from flask import Flask
from flask.templating import render_template
from .models import FirestoreHelper

from .helpers import VisionHelper
from .constants import BUCKET, PROJECT_ID


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
        try:
            response = json.dumps(response_json)
        except Exception as e:
            logging.warn('warning_return_json_not_support_2_agumentes[%s]', e)
            response = json.dumps(response_json, 'utf8')

        return response

    @app.route('/add/<user>', methods=['GET', 'POST'])
    def add(user):
        from .models import FirestoreHelper

        fire_db = FirestoreHelper(PROJECT_ID)
        result_a = fire_db.addData(u'users', user, {
            u'first': u'Alan',
            u'middle': u'Mathison',
            u'last': u'Turing',
            u'born': 1912
        })

        print('--------' + str(result_a))

        # read data
        docs = fire_db.getData(u'users')

        docs_arr = ""
        for doc in docs:
            docs_arr += u'{} => {}'.format(doc.id, doc.to_dict())

        return docs_arr

    @app.route('/populate/')
    def populate():
        from .to_populate import ITEMS

        fire_db = FirestoreHelper(PROJECT_ID)

        for item in ITEMS:
            result_a = fire_db.addData(u'nutrition', item['name'], {
                "alternatives": item["alternatives"],
                "nutrition": item["nutrition"]
            })

        # read data
        docs = fire_db.getData(u'nutrition')

        return str(docs)

    return app

