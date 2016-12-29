import spacy

class PatternFeatureExtractor:
    def __init__(self, doc):
        self.doc = doc

    def extract(self, kb):
        #kb = {"VERB": "set", "modify", "change"}
        ret = {}
        for key in kb:
            if key not in ret:
                ret[key] = []
            for word in self.doc:
                if word.tag_ == key:
                    ret[key].extend([(x, x.similarity(word)) for x in kb[key]])
        return ret

        
# experimenting
class FeatureExtractor:
    def __init__(self, graph):
        self.edge_filter = []
        self.graph = graph
        self.results = []
        
    def dfs(self, node, incl_token=[]):
        graph = self.graph
        
        if len(self.edge_filter) == 0 or node not in graph:
            return
        
        for word in graph[node]:            
            if len(self.edge_filter) == 0:
                return
                        
            if word.edge == self.edge_filter[0] or word.edge in self.edge_filter[0]:
                #if compound, amod or nmod, get all such neighbors
                if incl_token[0]:
                    if word.edge in ["compound", "amod", "nmod"]:
                        self.results.extend(list(word.token_obj.lefts))
                    else:
                        self.results.append(word)
                    
                self.edge_filter = self.edge_filter[1:]
                incl_token = incl_token[1:]
                
                self.dfs(word,incl_token)
                
    def extract_feature(self, start_node, edge_list, incl_list=[]):
        if len(incl_list)==0:
            incl_list = [True] * len(edge_list)
        elif len(incl_list) < len(edge_list):
            incl_list.extend([True]*(len(edge_list)-len(incl_list)))
            
        self.edge_filter = edge_list[:]
        self.results = []
        self.dfs(start_node,incl_list[:])
        return self.results

