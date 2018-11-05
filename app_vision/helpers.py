import os, io
import logging

from google.cloud import vision
from google.cloud.vision import types


class VisionHelper:

    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def getFace(self, bucket_img):
        response = self.client.annotate_image({
            'image': {'source': {'image_uri': bucket_img}},
            'features': [{'type': vision.enums.Feature.Type.FACE_DETECTION}], })

        return response

    def getLocalLabels(self, img_path):
        file_name = os.path.join(os.path.dirname(__file__), img_path)

        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)

        # Analyze image
        response = self.client.label_detection(image=image)
        logging.info('Labels RESPONSE: [%s]', response)

        # Get tags
        labels = []
        for label in response.label_annotations:
            labels.append(label.description)

        return labels

