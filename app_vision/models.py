import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class FirestoreHelper:
    def __init__(self, project_id):
        cred = credentials.ApplicationDefault()
        # cred = credentials.Certificate('path/to/serviceAccount.json')

        firebase_admin.initialize_app(cred, {
            'projectId': project_id,
        })

        self.db = firestore.client()


    def addData(self, collection, document, data_dic):
        doc_ref = self.db.collection(collection).document(document)
        response = doc_ref.set(data_dic)

        return response

    def getData(self, collection):
        users_ref = self.db.collection(collection)
        docs = users_ref.get()

        return docs

