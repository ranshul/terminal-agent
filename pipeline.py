import spacy
import re
import util.SyntaxGraph as SyntaxGraph
import util.classifier as Classifier
import actions.dispatcher as ActionDispatcher

print "Loading spacy..."
nlp = spacy.load("en")
print "Loaded english"

special_words = ["vlc media player", "pot player", "vlc", "potplayer", "lamb of god", "arctic monkeys", "house of cards"]

history = []
feedback_batch_train = []

model_instance = None
def get_input():
	print "> ",
	return unicode(raw_input())

def feedback():
	if len(history) <2:
		print "Stop annoying me."
		return None
	print preprocess(sentence[-2])
	print "If I failed to put double quotes around special words, list them separated by commas. Otherwise, leave it blank."
	special_words.extend(raw_input().split(",")) #do a better job
	print "I thought this is a " + Classifier.get_class(doc, model_instance) + " sentence. If it's an error, enter the number corresponding to the category."
	dic = {0:"modify", 1:"play", 2:"show", 3:"what"}
	print dic
	feedback_batch_train.append((nlp(unicode(sentence[-2])), input()))

	#write to data/feedback/label_<class name>.txt periodically and call classifier_model.feedback


def preprocess(sentence):
	for spl in special_words:
		sentence = re.sub(r'[^"\w](' + unicode(spl) + ')',r' "\1"', sentence, flags=re.IGNORECASE)

	# merge things within double quotes into a single proper noun token.
	doc = nlp(sentence)
	idx = -1
	for word in reversed(doc):
	    if word.text == '"':
	        if idx == -1:
	            idx = word.idx
	        else:
	            tok = doc.merge(word.idx,idx+1)
	            tok.tag_ = "NNP"
	            idx = -1
	return doc

def pipeline():
	global model_instance
	sentence = get_input()
	history.append(sentence)
	doc = preprocess(sentence)

	if sentence=="exit":
		return False
	elif sentence=="feedback":
		feedback()
		return True
	syntax_graph = SyntaxGraph.get_graph(doc)
	print syntax_graph
	
	if model_instance is None:
		model_instance = Classifier.ClassifierModel(nlp)

	# return model probabilities. if top-k have similar probabilities,
	# ask user for feedback

	sent_class = Classifier.get_class(doc, model_instance)
	print sent_class

	afe = ActionDispatcher.get_module(sent_class).ActionFeatureExtractor(doc, syntax_graph, nlp)
	print afe.extract_features()

	return True


def repl():
	while pipeline():
		i = 1

repl()