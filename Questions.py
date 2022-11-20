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
	for i in firestore.GetQuestions():
		if re.search(tokens, i, re.IGNORECASE):
			questions.append(i)
	return questions