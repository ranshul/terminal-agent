import random
import spacy

class Node:
    def __init__(self, text, token_type,edge,token_obj):
        self.uid = random.shuffle(list(text)) #distinguish between identical text tokens
        self.text = unicode(text)
        self.token_type = token_type
        self.edge = edge
        self.token_obj = token_obj

    def __str__(self):
        return "(" + unicode(self.text) + "," + unicode(self.edge) + ")"
    def __repr__(self):
        return "(" + unicode(self.text) + "," + unicode(self.edge) + ")"
    def __hash__(self):
        return hash(self.text + str(self.uid))
    def __eq__(self,other):
        return self.text + str(self.uid) == other.text + str(other.uid)

def _dfs(root, graph):  
    tree = Node(root.text, root.tag_, root.dep_, root)
    for child in root.children:
        if tree not in graph:
            graph[tree] = []
        graph[tree].append(_dfs(child,graph))
        
    return tree  

def get_graph(doc):
    graph = {}
    for sent in doc.sents:
        _dfs(sent.root, graph)
    #to make this return a tree, add neighbors to Node and append children there
    return graph