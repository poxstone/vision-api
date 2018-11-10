import os, io
import logging

import flask
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import vision
import google_auth_oauthlib.flow
import google.oauth2.credentials


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
            logging.error('error_getLocalLabels_[%s]', e)
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
                logging.info(properties_color)
                arr_color.append(properties_color)

        except Exception as e:
            logging.error('error_getImageProperties_[%s]', e)
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


class Oauth2Helper:
    """
    https://developers.google.com/identity/protocols/OAuth2WebServer
    https://requests-oauthlib.readthedocs.io/en/latest/examples/real_world_example_with_refresh.html
    """

    callback_page = 'oauth2callback'

    def getAuthUrl(self, client_secret_file, scopes):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            client_secret_file, scopes=scopes,
            redirect_uri='urn:ietf:wg:oauth:2.0:oob')

        flow.redirect_uri = flask.url_for(callback_page, _external=True)

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true')

        return authorization_url, state

    def createCredentials(self, client_secret_file, scopes, state):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            client_secret_file, scopes=scopes, state=state)
        flow.redirect_uri = flask.url_for(self.callback_page, _external=True)

        authorization_response = flask.request.url
        flow.fetch_token(authorization_response=authorization_response)

        return flow.credentials
