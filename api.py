from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Firebase import Firestore
from Questions import getData
from Constants import *
import spacy
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

firestore= Firestore(None)

def fetchModel():
    try:
        spacy.load(model)
    except:
        spacy.cli.download(model)

@app.get("/questions/{question}")
async def get_questions(question :str):
    question = question.replace("%20", " ")
    return { "questions": getData(question, firestore)}

@app.get("/answer/{question}")
async def get_questions(question :str):
    question = question.replace("%20", " ")
    return { "answer": firestore.GetAnswer(question)}


@app.get("/{data}")
async def read_item(data):
    if type(data) is str:
        if data == "questions":
            return { "questions": firestore.GetQuestions()}
        if data == "answers":
            return { "answers": firestore.GetAnswers()}

@app.get("/")
async def root():
    return {"message": "Hello World"}

fetchModel()