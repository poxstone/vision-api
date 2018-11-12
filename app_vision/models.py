from .helpers import FirestoreHelper
from .constants import PROJECT_ID
from .utils import  Logs


class OAuthModel:

    collection = u'config'
    document_oauth = u'oauth2'

    def __init__(self, project_id=PROJECT_ID):
        self.db = FirestoreHelper(project_id)

    def saveCredentials(self, credential_dic, state):
        doc_credential = self.credentials_to_dict(credential_dic, state)
        result = self.db.addData(self.collection, self.document_oauth,
                                 doc_credential)
        return result

    def getCredentials(self):
        result = self.db.getData(self.collection)
        if self.document_oauth not in result:
            Logs.warning('warn_getCredentials_not_result_', result)
            return result

        result = result[self.document_oauth]
        try:
            del result['expiry']
            del result['expired']
            del result['state']
        except Exception as e:
            Logs.error('error_getCredentials_del_result_', e)

        Logs.info('info_getCredentials_result_', result)
        return result

    def removeCredential(self):
        result = self.db.deleteDoc(self.collection, self.document_oauth)
        return result

    @staticmethod
    def credentials_to_dict(credentials, state):
        print(state)

        dic = {'token': credentials.token,
               'id_token': credentials.id_token,
               'state': state,
               'expiry': credentials.expiry,
               'expired': credentials.expired,
               'refresh_token': credentials.refresh_token,
               'token_uri': credentials.token_uri,
               'client_id': credentials.client_id,
               'client_secret': credentials.client_secret,
               'scopes': credentials.scopes}
        return dic