from importlib import import_module

dispatch_dict={
	"modify": "action_modify",
	"play": "action_play",
	"show": "action_show",
	"what": "action_what"
}

def get_module(sentence_class):
	if sentence_class not in dispatch_dict:
		#learning loop
		print "I'm not good with " + sentence_class + " sentences."
		return None
	module = import_module("actions." + dispatch_dict[sentence_class]) #throws error for show, what - haven't written those modules yet
	return module


