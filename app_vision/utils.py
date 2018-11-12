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
    def printMessages(message, logs):
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
            Logs.printMessages(message, logs)

    @staticmethod
    def error(message, logs):
        if not Logs.isLocal():
            logging.error(message)
            logging.error(logs)
        else:
            Logs.printMessages(message, logs)

    @staticmethod
    def warning(message, logs):
        if not Logs.isLocal():
            logging.warning(message)
            logging.warning(logs)
        else:
            Logs.printMessages(message, logs)
