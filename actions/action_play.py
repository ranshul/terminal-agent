from util.FeatureExtractor import FeatureExtractor

class ActionFeatureExtractor:
	def __init__(self, doc, graph, nlp):
		self.doc = doc
		self.graph = graph
		self.nlp = nlp

	def get_ROOT_vertex(self):
	    graph = self.graph
	    for v in graph:
			if v.edge == "ROOT":
			   return v

	def get_similarity(self,word1, word2):
		return self.nlp(unicode(word1)).similarity(self.nlp(unicode(word2)))

	def extract_features(self):
		doc = self.doc
		graph = self.graph
		ret = {}

		rootv = self.get_ROOT_vertex()
		fe = FeatureExtractor(graph)

		#find different heuristic
		if rootv.token_obj.pos_ != "VERB" and rootv.token_obj.tag_ != "NNP":
			return None

		play_tgt = rootv
		#start playing, stop playing
		if rootv.token_obj.lemma_ == "start" or rootv.token_obj.lemma_ == "stop":
			ret["action"] = rootv.token_obj.lemma_
			play_tgt = graph[rootv][0]
		if play_tgt.token_obj.lemma_ == "play" and play_tgt.token_obj.tag_ != "NNP":
			#play <song|album> by <artist> <with|in> <application>
			#play <artist>'s <song> <with|in> <application>
			#play <movie> <with|in> <application>
			#play <complicated expression>
			if "action" not in ret:
				ret["action"] = "start"
			edge_list = ["dobj"]
			play_what = fe.extract_feature(play_tgt, edge_list)
		elif rootv.token_obj.tag_ == "NNP":
			play_what = [rootv]
		else:
			return None

		ret["target_media"] = play_what
		media_by = []
		target_application = []

		for word in graph[play_tgt]:
			if word.edge == "prep":
				by_sim = self.get_similarity(word.text, "by")
				with_sim = self.get_similarity(word.text, "with")
				in_sim = self.get_similarity(word.text, "in")
				
				for tgt in graph[word]:
					if tgt.edge == "pobj":
						if by_sim > with_sim or by_sim > in_sim:
							media_by = [tgt]
						else:
							target_application = [tgt]
		
		ret["target_media_by"] = media_by
		ret["target_application"] = target_application

		#deal with play a movie with imdb rating 8+ later
		return ret