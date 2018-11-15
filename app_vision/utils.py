import logging
from flask import request

class Logs:
    @staticmethod
    def isLocal():
        if 'localhost' in request.host:
            return True
        else:
            return False

    @staticmethod
    def printMessages(message, logs=None):
        print('--->>')
        try:
            print(message)
            print(str(logs))
            print(type(logs))
            print(dir(logs))
            print(dict(logs))
        except Exception as e:
            print(str(e))
        print('<<---')
        print('')

    @staticmethod
    def info(message, logs):
        if not Logs.isLocal():
            logging.info(message)
            logging.info(logs)
        else:
            Logs.printMessages(message, logs=None)

    @staticmethod
    def error(message, logs=None):
        if not Logs.isLocal():
            logging.error(message)
            logging.error(logs)
        else:
            Logs.printMessages(message, logs=None)

    @staticmethod
    def warning(message, logs=None):
        if not Logs.isLocal():
            logging.warning(message)
            logging.warning(logs)
        else:
            Logs.printMessages(message, logs)


class FruitTools:
    @staticmethod
    def searchInTags(rows, fruit_tags):
        response = {}
        for ind, row in enumerate(rows):
            if ind == 0:
                # add titles
                response['title'] = row
            elif ind > 1 and len(fruit_tags) > 0:
                tag_sheet = row[0].lower()
                if FruitTools.compareTags(fruit_tags, tag_sheet):
                    Logs.info('info_FruitTools.searchInTags_{} in '.format(
                        fruit_tags), tag_sheet)
                    response['data'] = row
                    break
        if 'data' not in response:
            response['title'] = ['message']
            response['data'] = ['lables not match']
        return FruitTools.joinTitleData(response['title'], response['data'])

    @staticmethod
    def noAllowedTags(tag):
        if tag.lower() in ['fruit','natural','produce', 'cooking', 'common']:
            return False
        else:
            return True

    @staticmethod
    def compareTags(fruit_tags, tag_sheet):
        for tag in fruit_tags:
            if FruitTools.noAllowedTags(tag) and tag.lower() in tag_sheet.lower():
                # add value find
                return True

    @staticmethod
    def joinTitleData(titles=[], data=[]):
        result = []
        for indx, value in enumerate(data):
            result.append({'title': titles[indx], 'value': value})

        return result
