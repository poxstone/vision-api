import logging
import flask
from flask import request

class Logs:
    @staticmethod
    def isLocal():
        print('--dominio--' + request.host)
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
            print(dir(logs))
            print(dict(logs))
        except Exception as e:
            print(str(e))
        print('<<---')

    @staticmethod
    def info(message, logs):
        if not Logs.isLocal():
            logging.info(message)
            logging.info(logs)
        else:
            Logs.printMessages(message, logs)

    @staticmethod
    def error(message, **logs):
        if not Logs.isLocal():
            logging.error(message)
            logging.error(logs)
        else:
            Logs.printMessages(message, logs)
