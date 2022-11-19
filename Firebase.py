import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os

# Use a service account.

sdk = 'firebase-sdk.json'
config_load = True
config={}
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

if not os.path.exists(sdk):
    config_load = False
    config = {
        "type": "service_account",
    }
    for iter in configs:
        config[iter] = os.environ.get(iter).encode('latin1').decode('unicode_escape')
else:
    with open(sdk) as fd:
        data = json.loads(fd.read())
    if data['project_id'] == "":
        print("Configuration is not correct Trying ENV")
        config_load = False
if config_load == False:
	sdk = config

cred = credentials.Certificate(sdk)
app = firebase_admin.initialize_app(cred)
db = firestore.client()
document_name = 'psykick-data'
collection = db.collection(u'data')
doc_ref = collection.document(document_name)


def UploadQuestion(data):
    doc_ref_questions = collection.document(u'Questions')
    print(type(data))
    if type(data) is dict:
        for i in data:
            print(i)


def UploadAnswers(data):
    doc_ref_answers = collection.document(u'Answers')
    print(type(data))
    if type(data) is dict:
        print(json.loads(json.dumps(data)))
        doc_ref_answers.set(json.loads(json.dumps(data)))


def GetQuestions():
    docs = collection.stream()
    for doc in docs:
        if doc.id == document_name:
            ret = list(doc.to_dict().keys())
            return ret


def GetAnswers():
    docs = collection.stream()
    for doc in docs:
        if doc.id == document_name:
            ret = list(doc.to_dict().values())
            return ret


def UploadData(data):
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
        doc_ref.set(res)
