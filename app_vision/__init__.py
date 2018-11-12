import flask
from flask import Flask
from flask.templating import render_template
import google.oauth2.credentials

from .helpers import VisionHelper, FirestoreHelper, Oauth2Helper, SpreadHelper
from .constants import BUCKET, PROJECT_ID, CLIENT_SECRET_FILE, SCOPES, \
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
        oauth2Helper = Oauth2Helper()
        authorization_url, state = oauth2Helper.getAuthUrl(CLIENT_SECRET_FILE,
                                                        SCOPES)
        flask.session['state'] = state

        Logs.info('info_authorize_authorization_url', authorization_url)
        return flask.redirect(authorization_url)

    @app.route('/oauth2callback')
    def oauth2callback():
        configs = Configs()
        state = flask.session['state']
        del flask.session['state']

        oauth2Helper = Oauth2Helper()
        credentials = oauth2Helper.createCredentials(CLIENT_SECRET_FILE, SCOPES,
                                                     state)
        configs.saveCredentials(credentials, state)

        Logs.info('info_oauth2callback_credentials_', credentials)
        return 'Authorized App Success!'

    @app.route('/revoke')
    def revoke():
        configs = Configs()
        credential = configs.getCredentials()

        if 'refresh_token' not in credential:
            return 'Not credentials found! try manual: ' + \
            'https://myaccount.google.com/u/0/permissions?pageId=none&pli=1'

        Logs.info('info_revoke_credential_', credential)
        revoke = Oauth2Helper.revokeCredentials(credential['refresh_token'])
        configs.removeCredential()

        status_code = getattr(revoke, 'status_code')
        Logs.info('info_revoke_status_code', status_code)
        return 'Revoked: ' + str(status_code)

    @app.route('/sheet')
    def getSheet():
        configs = Configs()
        oauth2_dict = configs.getCredentials()

        Logs.info('info_getSheet_oauth2_dict', oauth2_dict)

        if 'token' not in oauth2_dict:
            return '{"error: "Not credentials found, please authorize again"}',\
                   401

        credential = google.oauth2.credentials.Credentials(**oauth2_dict)

        spreadHelper = SpreadHelper(credential)

        try:
            sheet_info = spreadHelper.getSheetInfo(SPREAD_SHEET)

            sheet = sheet_info['sheets'][0]['properties']['title']
            max_rows = sheet_info['sheets'][0]['properties']['gridProperties'][
                'rowCount']
            range_str = '{}!A2:L{}'.format(sheet, max_rows)
            result = spreadHelper.getSheetValues(SPREAD_SHEET, range_str)
            return flask.jsonify(result)
        except Exception as e:
            Logs.error('error_getSheet_sheet_info', e)
            return '{"error: "Error calling Sheet, please validate that ' \
                   'exists"}', 500

    return app
