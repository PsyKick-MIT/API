import spacy
import re
from Firebase import Firestore


def getData(question :str, firestore :Firestore):
	try:
		nlp = spacy.load("en_core_web_lg")
	except:
		spacy.cli.download("en_core_web_lg")
		spacy.load("en_core_web_lg")
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
