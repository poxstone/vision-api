import os, io
import requests

from apiclient import discovery
import flask
import firebase_admin
from firebase_admin import credentials, firestore
import google_auth_oauthlib.flow
from google.cloud import vision

from .utils import Logs


class Oauth2Helper:
    """
    https://developers.google.com/identity/protocols/OAuth2WebServer
    https://requests-oauthlib.readthedocs.io/en/latest/examples/real_world_example_with_refresh.html
    """

    callback_page = 'oauth2callback'

    def getAuthUrl(self, client_secret_file, scopes):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            client_secret_file, scopes=scopes)

        flow.redirect_uri = flask.url_for(self.callback_page, _external=True)

        authorization_url, state = flow.authorization_url(access_type='offline',
                                                include_granted_scopes='true')
        return authorization_url, state

    def getAccessTokenn(self, credential):
        return credential

    def createCredentials(self, client_secret_file, scopes, state):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            client_secret_file, scopes=scopes, state=state)
        flow.redirect_uri = flask.url_for(self.callback_page, _external=True)

        authorization_response = flask.request.url


        Logs.info('info_createCredentials_auth_resp', authorization_response)
        flow.fetch_token(authorization_response=authorization_response)

        oauth2_dict = flow.credentials

        try:
            oauth2_dict.refresh_token
            Logs.info('info_createCredentials_oauth2_dict.refresh_token',
                      oauth2_dict)
        except Exception as e:
            Logs.warning('warn_createCredentials_not_found_oauth2_dict', e)
            return oauth2_dict

        return oauth2_dict

    @staticmethod
    def revokeCredentials(credential_token):
        revoke = requests.post('https://accounts.google.com/o/oauth2/revoke',
               params={'token': credential_token},
               headers={'content-type': 'application/x-www-form-urlencoded'})
        return revoke


class VisionHelper:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    @staticmethod
    def readImage(img_path):
        file_name = os.path.join(os.path.dirname(__file__), img_path)

        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
        return content

    def getFace(self, bucket_img):
        response = self.client.annotate_image({
            'image': {'source': {'image_uri': bucket_img}},
            'features': [{'type': vision.enums.Feature.Type.FACE_DETECTION}]})

        face_response = []
        for label in response.face_annotations:
            face_response.append(label)

        return face_response

    def getLocalLabels(self, bucket_img):
        try:
            response = self.client.annotate_image({
                'image': {'source': {'image_uri': bucket_img}},
                'features': [{'type': vision.enums.Feature.Type.LABEL_DETECTION}]})

            label_response = []
            for label in response.label_annotations:
                label_response.append({
                    'label': label.description,
                    'score': label.score,
                    'topicality': label.topicality
                })
        except Exception as e:
            Logs.error('error_getLocalLabels_', e)
            label_response = ["error on load getLocalLabels"]

        return label_response

    def getImageProperties(self, bucket_img):
        try:
            response = self.client.annotate_image({
                'image': {'source': {'image_uri': bucket_img}},
                'features': [{'type': vision.enums.Feature.Type.IMAGE_PROPERTIES}]})

            props = response.image_properties_annotation

            arr_color = []
            for color in props.dominant_colors.colors:
                properties_color = {
                    'pixel_fraction': color.pixel_fraction,
                    'rgb': 'rgb({},{},{})'.format(color.color.red,
                                                       color.color.green,
                                                       color.color.blue)}
                Logs.info('info_getImageProperties', properties_color)
                arr_color.append(properties_color)

        except Exception as e:
            Logs.error('error_getImageProperties_', e)
            arr_color = ["error on load getImageProperties"]

        return arr_color


class FirestoreHelper:
    def __init__(self, project_id):
        # cred = credentials.Certificate('path/to/serviceAccount.json')
        global firebase_db

        try:
            print(firebase_db)
            self.db = firebase_db
        except Exception as e:
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred, {
                'projectId': project_id})
            self.db = firestore.client()
            firebase_db = self.db

    def addData(self, collection, document, data_dic):
        doc_ref = self.db.collection(collection).document(document)
        response = doc_ref.set(data_dic)

        return response

    def getData(self, collection):
        collection_ref = self.db.collection(collection)
        docs = collection_ref.get()

        items = {}
        for item in docs:
            items[str(item.id)] = item.to_dict()

        return items

    def deleteDoc(self, collection, doc):
        delete_ref = self.db.collection(collection).document(doc).delete()

        return delete_ref


class SpreadHelper:
    def __init__(self, credentials):
        self.service = discovery.build('sheets', 'v4', credentials=credentials)

    def getSheetInfo(self, sheet_id):
        result = self.service.spreadsheets().get(
            spreadsheetId=sheet_id).execute()

        return result
