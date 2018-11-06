import os, io
import logging

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

        return label_response

    def getImageProperties(self, bucket_img):
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

        return arr_color
