from .models import InitialParser
from apps.nlp_core.Models.index import NLP_Model

import en_core_web_sm
from apps.nlp_core.Models.deepmoji import DeepMoji
import spacy
from spacy import displacy
import json
from apps.nlp_core.Models.index import ArticleParser

d = DeepMoji()

class InitialArticleParser(ArticleParser):
    def initialize(self, parser = InitialParser):
        super().initialize()
        self.d = d
        self.nlp = spacy.load("en_core_web_sm")
        self.d.initialize()
        self.parser = parser
    def tokenize(self,query):
        print("tokenizing")
        self.parsers = [self.parser(self.nlp,self.d) for q in query]
        super().tokenize(query)
