import spacy
from keras.models import model_from_json
import numpy as np
import os
from sklearn.model_selection import train_test_split
from keras.utils import np_utils, generic_utils

debug = False	
maxlen = 40

class ClassifierModel:
	def __init__(self,nlp,model_path="",weights_path=""):
		if model_path == "" or weights_path == "":
			model_path = "data/model.json"
			weights_path = "data/model.h5"
		self.model = load_model(model_path, weights_path)
		self.nlp = nlp


def load_model(mpath="",wpath=""):
	if mpath=="" and wpath=="":
		mpath = "data/model.json"
		wpath = "data/model.h5"
	# load json and create model
	json_file = open(mpath, 'r')
	model_json = json_file.read()
	json_file.close()
	model = model_from_json(model_json)	
	# load weights into new model
	model.load_weights(wpath)

	if debug:
		print "Model loaded. Compiling..."
	model.compile('adam','categorical_crossentropy')

	if debug:
		print "Model compiled."
		print model.summary()

	return model

def class_to_label(key):
	dic = {0:"modify", 1:"play", 2:"show", 3:"what"}
	return dic[key]

def get_class(doc, classifier_model):
	model = classifier_model.model
	#pad input
	vec_seq = []
	for token in doc:
	    vec_seq.append(token.vector)
	orig_len, vec_len = np.shape(vec_seq)
	new = []
	if orig_len < maxlen:
	    new = np.zeros((maxlen,vec_len))
	    new[maxlen-orig_len:,:] = vec_seq
	else:
	    new = vec_seq[orig_len-maxlen:,:]

	new = np.array([new])

	result = model.predict(np.array(new))
	return class_to_label(np.argmax(result))

def feedback(classifier_model):
	labels = []
	for f in os.listdir(os.path.join("data","feedback")): #data/train for training
	    path = os.path.join("data","feedback",f)
	    if os.path.isfile(path):
	        labels.append(path)

	train_vec_seqs = []
	train_Y = []
	for label_file in labels:
	    sentences = open(label_file, "r").readlines()
	    for sentence in sentences:
	        if len(sentence.lstrip().rstrip()) > 0:
	            doc = classifier_model.nlp(unicode(sentence))
	            vec_seq = []
	            for token in doc:
	                vec_seq.append(token.vector) 
	            train_vec_seqs.append(np.array(vec_seq))
	            train_Y.append(int(label_file.split("label_")[1].split(".txt")[0]))

	maxlen = 40
	new_seqs = []
	for vec_seq in train_vec_seqs:
	    orig_len, vec_len = np.shape(vec_seq)
	    if orig_len < maxlen:
	        new = np.zeros((maxlen,vec_len))
	        new[maxlen-orig_len:,:] = vec_seq
	    else:
	        new = sequence[orig_len-maxlen:,:]
	    new_seqs.append(new)

	train_X = new_seqs
	x_train, x_test, y_train, y_test = train_test_split(train_X, train_Y, test_size=0.1)
	y_train, y_test = [np_utils.to_categorical(x,nb_classes=4) for x in (y_train,y_test)]

	classifier_model.model.fit(np.array(x_train), y_train, nb_epoch = 5)
	print "Done training feedback."
	
	#save model
	# model_json = model.to_json()
	# jf = open("model.json","w")
	# jf.write(model_json)
	# model.save_weights("model.h5")
	                        