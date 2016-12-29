# set vlc brightness to 30%

# <verb> <target_object_modifier>'s <target_object>'s <object_property> <preposition> <value>
# <verb> <target_object_modifier>'s <target_object> <object_property> <preposition> <value>
# <verb> <object_property> <preposition> (of) <target_object_modifier>'s <target_object> <preposition> <value>
# <verb> <object_property> <preposition> (of) <target_object> <target_object_modifier>`   

from util.FeatureExtractor import FeatureExtractor

'''
modify

verb specifies the action. ex: set, increase, decrease
verb acts on a target noun that is typically the direct object from the verb.
target ex: volume, brightness or some other property

the target value of the property can be typically specified in two ways

the verb has a preposition out of it whose object of preposition is the value (pobj from IN)
or, the target has a possessive form and the poss from the property goes to "value" which in 
turn goes to a preposition and that, has a pobj link to the final value

if there is no noun, (volume to 24% or volume 24), it is hard to distinguish between this and music commands like 505 by arctic monkeys. same grammatical form
we'll deal with this later
''' 


class ActionFeatureExtractor:
    def __init__(self,doc, graph, nlp):
        self.doc = doc
        self.graph = graph
        self.nlp = nlp

    def get_ROOT_vertex(self):
        graph = self.graph
        for v in graph:
            if v.edge == "ROOT":
                return v

    def extract_features(self):
        graph = self.graph
        rootv = self.get_ROOT_vertex()
        fe = FeatureExtractor(graph)

        if rootv.token_obj.pos_ != "VERB":
            #find different heuristic
            return None

        target_value = []

        edge_list = ["dobj", ["compound", "amod", "nmod"]]
        target_property = fe.extract_feature(rootv, edge_list)

        #set <pot player>'s brightness to 20 %
        edge_list = ["dobj","poss",["compound", "nmod", "amod"]]
        target_object = fe.extract_feature(rootv, edge_list, [False])

        # sentence is in a different form
        if target_object == []:
            #set brightness of vlc player to 30
            edge_list = ["dobj","prep",["pobj","pcomp","xcomp"], ["nmod", "compound","amod"]]
            target_object = fe.extract_feature(rootv, edge_list, [False, False])

            #set brightness of House's vlc player to 33
            edge_list = ["dobj","prep","pobj","poss",["nmod", "compound","amod"]]
            target_object_modifier = fe.extract_feature(rootv, edge_list, [False, False, False])

            if target_object_modifier == []:
                #set brightness of vlc player playing/showing/displaying House to 33 -- changes prep from root to acl
                edge_list = ["dobj","prep","pobj",["relcl","acl", "xcomp"],"dobj",["nmod", "compound","amod"]]
                target_object_modifier = fe.extract_feature(rootv, edge_list, [False, False, False])

                edge_list = ["dobj","prep","pobj",["relcl","acl", "xcomp"],"prep", "pobj", "nummod"]
                target_value = fe.extract_feature(rootv, edge_list, [False, False, False, False, False])
        else:
            #set black mirror's vlc player's brightness to 33
            edge_list = ["dobj","poss","poss",["nmod", "compound","amod"]]
            target_object_modifier = fe.extract_feature(rootv, edge_list, [False, False])

        if target_value == []:
            #set potplayer's brightness to 30%
            edge_list = ["prep", "pobj", "nummod"]
            target_value = fe.extract_feature(rootv, edge_list, [False])

        if target_value == []:
            #set vlc volume to 30
            edge_list = ["dobj"]
            target_property = fe.extract_feature(rootv, edge_list)

            edge_list = ["dobj", ["compound", "amod", "nmod"]]
            target_object = fe.extract_feature(rootv, edge_list, [False])

            #set house's potplayer brightness to 30%
            edge_list = ["dobj", "poss", ["compound", "amod", "nmod"]] #bug when set house of cards's potplayer ...: houes becomes root
            target_object_modifier = fe.extract_feature(rootv,edge_list,[False])

            edge_list = ["dobj", "prep", "pobj"]
            target_value = fe.extract_feature(rootv, edge_list, [False, False])

        return {"property": target_property, "object": target_object, "value": target_value, "object_modifier": target_object_modifier}

#import kb.ActionProperties as ActionProperties

# class PatternFeatureExtractor:
#     def __init__(self, doc, nlp):
#         self.doc = doc
#         self.nlp = nlp


#     def extract_primary_verb(self):
#         #add case for checking if verb is noun
#         nlp = self.nlp
#         kb = {"VERB": [nlp(u"set"), nlp(u"modify"), nlp(u"change")]}
#         fe = PatternFeatureExtractor(self.doc)
#         return fe.extract_feature(kb)

#     def extract_target_property(self):
#         nlp = self.nlp

#         kb = {"NOUN"}

#     def extract_target_modifier_verb(self):
#         nlp = self.nlp
#         kb = {"VERB": [nlp(u"playing"), nlp(u"showing"), nlp(u"running")], 
#               "ADP": [nlp(u"with")], 
#               "ADJ": [nlp(u"that"), nlp(u"which")]
#              }

#         #VBG
        

