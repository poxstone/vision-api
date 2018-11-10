import os, io
import logging


from urllib.parse import urlencode
from urllib import request
from urllib.request import urlopen
import oauth2client.client
import json

from google.cloud import vision


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

class Oauth2Helper:
    @staticmethod
    def refresh_access_token(client_id, client_secret, refresh_token):
        # You can also read these values from the json file
        request_token = request('https://accounts.google.com/o/oauth2/token',
                          data=urlencode({
                              'grant_type': 'refresh_token',
                              'client_id': client_id,
                              'client_secret': client_secret,
                              'refresh_token': refresh_token
                          }),
                          headers={
                              'Content-Type': 'application/x-www-form-urlencoded',
                              'Accept': 'application/json'
                          })
        response = json.load(urlopen(request_token))
        return response['access_token']



    @staticmethod
    def get_credentials(access_token):
        user_agent = "Google Drive API for Python"
        revoke_uri = "https://accounts.google.com/o/oauth2/revoke"
        credentials = oauth2client.client.AccessTokenCredentials(
            access_token=access_token,
            user_agent=user_agent,
            revoke_uri=revoke_uri)
        return credentials
