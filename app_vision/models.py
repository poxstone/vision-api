import logging
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class FirestoreHelper:
    def __init__(self, project_id):
        # cred = credentials.Certificate('path/to/serviceAccount.json')
        global firebase_db
        
        try:
            print(firebase_db)
            self.db = firebase_db
        except Exception as e:
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred, {
                'projectId': project_id })
            self.db = firestore.client()
            firebase_db = self.db


    def addData(self, collection, document, data_dic):
        doc_ref = self.db.collection(collection).document(document)
        response = doc_ref.set(data_dic)

        return response

    def getData(self, collection):
        collection_ref = self.db.collection(collection)
        docs = collection_ref.get()

        items = {}
        for item in docs:
            items[str(item.id)] = item.to_dict()

        return items

