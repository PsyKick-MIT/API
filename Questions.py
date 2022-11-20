import spacy
import re
from Firebase import Firestore
from Constants import *

def getData(question :str, firestore :Firestore):
	nlp = spacy.load(model)
	doc = nlp(question)
	questions = []
	tokens = ""
	for token in doc:
		if token.pos_ == "PROPN" or token.pos_ == "NOUN":
			tokens = token.text
	for question in firestore.GetQuestions():
		if re.search(tokens, question, re.IGNORECASE):
			questions.append(question)
	for answer in firestore.GetAnswers():
		if re.search(tokens, answer, re.IGNORECASE):
			questions.append(firestore.GetQuestion(answer))
	return list(set(questions))