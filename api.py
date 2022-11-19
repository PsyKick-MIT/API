from fastapi import FastAPI
from Firebase import GetQuestions, GetAnswers
app = FastAPI()

@app.get("/{data}")
async def read_item(data):
    if type(data) is str:
        if data == "questions":
            return GetQuestions()
        if data == "answers":
            return GetAnswers()

@app.get("/")
async def root():
    return {"message": "Hello World"}