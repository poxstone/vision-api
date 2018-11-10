import sys
import logging
import json

import flask
from flask import Flask, request, redirect
from flask.templating import render_template
import google_auth_oauthlib.flow
import google.oauth2.credentials
from requests_oauthlib import OAuth2Session
import httplib2

from apiclient import discovery
from .models import FirestoreHelper
from .helpers import VisionHelper, Oauth2Helper
from .constants import BUCKET, PROJECT_ID, CLIENT_SECRET_JSON, CLIENT_ID, \
    CLIENT_SECRET, CLIENT_SECRET, SCOPES


# Run flask
def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)

    @app.route('/')
    def root():
        print (globals())
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

        docs = fire_db.getData(u'users')
        return str(docs)

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

    @app.route('/installation', methods=['GET', 'POST'])
    def installation():
        # https://developers.google.com/identity/protocols/OAuth2WebServer
        #https://requests-oauthlib.readthedocs.io/en/latest/examples/real_world_example_with_refresh.html

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            sys.path[0] + '/' + CLIENT_SECRET_JSON,
            scopes=SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')

        flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true')

        flask.session['state'] = state
        print('asdsadas' + state)
        return flask.redirect(authorization_url)


    @app.route('/oauth2callback', methods=['GET', 'POST'])
    def oauth2callback():
        state = flask.session['state']
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
                      sys.path[0] + '/' + CLIENT_SECRET_JSON,
                      scopes=SCOPES, state=state)
        flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

        authorization_response = flask.request.url
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials
        flask.session['credentials'] = credentials_to_dict(credentials)

        fire_db = FirestoreHelper(PROJECT_ID)
        return_db = fire_db.addData(u'config', 'oauth2',
                flask.session['credentials'])
        logging.info('imstall_params[%s]', return_db)
        return "installed: " + str(return_db)


    @app.route('/sheet/')
    def getSheet():
        if 'credentials' not in flask.session:
            fire_db = FirestoreHelper(PROJECT_ID)
            oauth2_dict = fire_db.getData(u'config')['oauth2']
            credentials = google.oauth2.credentials.Credentials(
                          **oauth2_dict)
        else:
            credentials = google.oauth2.credentials.Credentials(
                          **flask.session['credentials'])

        service = discovery.build('drive', 'v3', credentials=credentials)
        google_request = service.files().list()
        result = google_request.execute()
        print(result)

        # Response
        try:
            response = json.dumps(result)
        except Exception as e:
            response = json.dumps(result, 'utf8')

        return response

    return app

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

