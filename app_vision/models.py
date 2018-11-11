from .helpers import FirestoreHelper
from .constants import PROJECT_ID


class Configs:

    kind_config = u'config'
    entity_oauth = u'oauth2'

    def __init__(self, project_id=PROJECT_ID):
        self.db = FirestoreHelper(project_id)

    def saveCredentials(self, credential_dic):
        result = self.db.addData(self.kind_config, self.entity_oauth,
                        self.credentials_to_dict(credential_dic))
        return result

    def getCredentials(self):
        result = self.db.getData(self.kind_config)[self.entity_oauth]
        return result

    @staticmethod
    def credentials_to_dict(credentials):
        return {'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes}
