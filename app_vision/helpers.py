import os, io
import logging

from google.cloud import vision
from google.cloud.vision import types


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
            'features': [{'type': vision.enums.Feature.Type.FACE_DETECTION}], })

        return response

    def getLocalLabels(self, img_path):
        content = self.readImage(img_path)
        image = types.Image(content=content)

        # Analyze image
        response = self.client.label_detection(image=image)
        logging.info('Labels RESPONSE: [%s]', response)

        # Get tags
        labels = []
        for label in response.label_annotations:
            labels.append(label.description)

        return labels

    def getImageProperties(self, img_path):
        content = self.readImage(img_path)
        image = types.Image(content=content)

        response = self.client.image_properties(image=image)
        props = response.image_properties_annotation

        arr_color = []
        for color in props.dominant_colors.colors:
            properties_color = {
                'pixel_fraction': color.pixel_fraction,
                'color_red': color.color.red,
                'color_green': color.color.green,
                'color_blue': color.color.blue,
                'color_alpha': color.color.alpha
            }
            logging.info(properties_color)
            arr_color.append(properties_color)

        return arr_color
