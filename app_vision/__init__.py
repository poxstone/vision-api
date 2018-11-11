import sys
import logging

import flask
from flask import Flask
from flask.templating import render_template
import google.oauth2.credentials

from apiclient import discovery
from .helpers import VisionHelper, FirestoreHelper, Oauth2Helper
from .constants import BUCKET, PROJECT_ID, CLIENT_SECRET_JSON, SCOPES, \
    SPREAD_SHEET
from .models import Configs

from .utils import Logs


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

        return flask.jsonify(response_json)

    @app.route('/populate/')
    def populate():
        from .to_populate import ITEMS

        fire_db = FirestoreHelper(PROJECT_ID)

        for item in ITEMS:
            fire_db.addData(u'nutrition', item['name'], {
                "alternatives": item["alternatives"],
                "nutrition": item["nutrition"]
            })

        docs = fire_db.getData(u'nutrition')
        return str(docs)

    @app.route('/authorize', methods=['GET', 'POST'])
    def installation():
        client_secret_file = sys.path[0] + '/' + CLIENT_SECRET_JSON

        oauth2Helper = Oauth2Helper()
        authorization_url, state = oauth2Helper.getAuthUrl(client_secret_file,
                                                        SCOPES)
        flask.session['state'] = state
        Logs.info('info_authorize_authorization_url', authorization_url)

        return flask.redirect(authorization_url)

    @app.route('/oauth2callback')
    def oauth2callback():
        configs = Configs()
        state = flask.session['state']
        client_secret_file = sys.path[0] + '/' + CLIENT_SECRET_JSON

        oauth2Helper = Oauth2Helper()
        credentials = oauth2Helper.createCredentials(client_secret_file, SCOPES,
                                                     state)
        configs.saveCredentials(credentials, state)

        Logs.info('info_oauth2callback_credentials_', credentials)
        Logs.info('info_oauth2callback_refresh_token_', credentials.refresh_token)
        return 'Authorized App Success!'

    @app.route('/sheet')
    def getSheet():
        if not ('credentials' in flask.session):
            configs = Configs()
            oauth2_dict = configs.getCredentials()

            credentials = google.oauth2.credentials.Credentials(
                          **oauth2_dict)
        else:
            credentials = google.oauth2.credentials.Credentials(
                          **flask.session['credentials'])

        Logs.info('info_getSheet_credentials_', credentials)
        service = discovery.build('sheets', 'v4', credentials=credentials)
        google_request = service.spreadsheets().get(spreadsheetId=SPREAD_SHEET)
        result = google_request.execute()

        Logs.info('info_getSheet_result_', [result])
        return flask.jsonify(result)

    return app
