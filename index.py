from .models import InitialParser
from apps.logic.model import NLP_Model

import en_core_web_sm
from apps.deepmoji.index import DeepMoji
import spacy
from spacy import displacy
import json
from apps.logic.model import ArticleParser

from apps.deepmoji.index import DeepMoji
d = DeepMoji()

class InitialArticleParser(ArticleParser):
    def initialize(self,parser = InitialParser):
        super().initialize()
        self.d = d
        self.nlp = spacy.load("en_core_web_sm")
        self.d.initialize()
        self.parser = parser
    def tokenize(self,query):
        print("tokenizing")
        self.parsers = [self.parser(self.nlp,self.d) for q in query]
        super().tokenize(query)
