import os, io
import logging
import argparse
import datetime

from google.cloud import vision
from google.cloud import datastore


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


class DatastoreHelper:
    """
    https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/datastore/cloud-client/tasks.py
    """
    def __init__(self, project_id):
        self.client = datastore.Client(project_id)


    def add_task(self, client, description):
        key = client.key('Task')
        task = datastore.Entity(key, exclude_from_indexes=['description'])

        task.update({
            'created': datetime.datetime.utcnow(),
            'description': description,
            'done': False
        })

        client.put(task)

        return task.key