from fastapi import FastAPI
from Firebase import Firestore
from Questions import getData
app = FastAPI()

firestore= Firestore(None)

@app.get("/questions/{question}")
async def get_questions(question :str):
    question = question.replace("%20", " ")
    print(question)
    return getData(question, firestore)


@app.get("/{data}")
async def read_item(data):
    if type(data) is str:
        if data == "questions":
            return firestore.GetQuestions()
        if data == "answers":
            return firestore.GetAnswers()

@app.get("/")
async def root():
    return {"message": "Hello World"}