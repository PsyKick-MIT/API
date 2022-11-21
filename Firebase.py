import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os

class Firestore:

    def __init__(self, file) -> None:
        config={}
        if file is None:
            configs = [
                "project_id",
                'private_key_id',
                'private_key',
                'client_email',
                'client_id',
                'auth_uri',
                'token_uri',
                'auth_provider_x509_cert_url',
                'client_x509_cert_url'
            ]
            config = {
                "type": "service_account",
            }
            for iter in configs:
                config[iter] = os.environ.get(iter).encode('latin1').decode('unicode_escape')
        else:
            config = file
        cred = credentials.Certificate(config)
        app = firebase_admin.initialize_app(cred)
        db = firestore.client()
        self.document_name = 'psykick-data'
        self.collection = db.collection(u'data')
        self.doc_ref = self.collection.document(self.document_name)


    def UploadQuestion(self, data):
        doc_ref_questions = self.collection.document(u'Questions')
        print(type(data))
        if type(data) is dict:
            for i in data:
                print(i)


    def UploadAnswers(self, data):
        doc_ref_answers = self.collection.document(u'Answers')
        print(type(data))
        if type(data) is dict:
            print(json.loads(json.dumps(data)))
            doc_ref_answers.set(json.loads(json.dumps(data)))


    def GetQuestion(self, query):
        docs = self.collection.stream()
        document :dict = None
        for doc in docs:
            if doc.id == self.document_name:
                document = doc.to_dict()
        questions = list(document.keys())
        return questions[list(document.values()).index(query)]

    def GetQuestions(self):
        docs = self.collection.stream()
        for doc in docs:
            if doc.id == self.document_name:
                ret = list(doc.to_dict().keys())
                return ret

    def GetAnswer(self, question):
        docs = self.collection.stream()
        if question[-1] != '.':
            question += "?"
        data = {}
        for doc in docs:
            if doc.id == self.document_name:
                data = doc.to_dict();
                break
        if data is not None:
            return data[question]
        return None

    def GetAnswers(self):
        docs = self.collection.stream()
        for doc in docs:
            if doc.id == self.document_name:
                ret = list(doc.to_dict().values())
                return ret


    def UploadData(self,data):
        if type(data) is dict:
            ques = data['Questions']
            ques_len = len(ques)
            ans = data['Answers']
            ans_len = len(ans)
            res = {}
            if ques_len != ans_len:
                print("Leaving last", abs(ques_len - ans_len), "Entries")
            if ques_len > ans_len:
                enum = ans_len
            else:
                enum = ques_len
            for entry in range(enum):
                res[ques[entry]] = ans[entry]
            print(res)
            self.doc_ref.set(res)