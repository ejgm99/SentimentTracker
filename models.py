from collections import Counter
import json
import emoji
import numpy as np
from . import spacy_tools

class Parser():
    def __init__(self):
        self.subjects = {} #subjects are entities or acts that can influence a person's sentiments
        self.ent_ids = [] #this is the ids of the entities as they are stored in subjects
        self.act_ids = [] #
        self.totalSubjects = 0; #this is a counter meant to store how many subjects have been logged
        self.SubjectIDs = {}
        self.operation = ""
    def isSubject(self,token):
        #this is where all the tokens are going to be tested
        #to figure out if they're actually something we want to track
        self.operation("Subject classification")
    def getSentimentTrackers(self):
        return list(self.subjects.values())
    def AddNewSubject(self, lemma):
        #There will be some abstracted way to encrypyt each function at some point.
        #This isn't something that we'll be spending an incredible amount of
        #time on at first though.
        self.totalSubjects+=1
        self.subjects[self.totalSubjects] = SentimentTracker(lemma)
        #If we want the ID of a given lemma we access this
        self.SubjectIDs[lemma] = self.totalSubjects
    def GetAllSubjects(self):
        return self.subjects
    def ScoreSentence(self, sentence):
        self.operation("Individual sentence prediction")
    def getOverallSentimentForEachToken(self):
        #won't actually return anything, will just get all of the tokens to calculate their final estimates
        [sentiment_tracker.calculateOverallSentiment() for sentiment_tracker in self.getSentimentTrackers()]
    def ScoreDoc(self, doc):
        self.doc = doc;
        self.operation="Scoring a document";
        print("Scoring a document")
        #might want to get a size metric going in this part
    def to_json(self):
        #this function will return the indexing of the sentences (maybe?)
        #but will definitely aggregate all of the jsonized predictions
        #from each token
        prelim_json = [sentiment_tracker.to_json() for sentiment_tracker in self.getSentimentTrackers()]
        return prelim_json

class InitialParser(Parser):
    def __init__(self,nlp = None, d = None):
        super().__init__()
        self.nlp = nlp
        self.d = d
    def ScoreDoc(self, doc):
        super().ScoreDoc(doc)
        #this might need to get renamed, although we are distilling
        #this object so from a storage perspective might not need to
        #get stored.
        doc = self.nlp(doc)
        #this initial tracker scores the whole sentence by just sequentially taking each sentence and
        #scoring it, without really taking into account the idea of context or anything
        for count, sentence in enumerate(doc.sents):
            print(sentence)
            sentence_score = self.ScoreSentence(sentence)
            for token in sentence:
                if(self.isSubject(token.dep_)):
                    try:
                        #see if the base form of this word has been used, and add to that already active sentiment tracker
                        sentiment_tracker_id = self.SubjectIDs[spacy_tools.getLemma(token)]
                        #get sentement tracker from the sentence
                        sentiment_tracker = self.subjects[sentiment_tracker_id]
                        #the sentence's score is given to the individual word
                        sentiment_tracker.newSentence(count,sentence_score)
                    except(KeyError):
                        #KeyError means there's no tracking instance of that word yet. So we make a new one
                        self.AddNewSubject(spacy_tools.getLemma(token))
                        self.subjects[self.totalSubjects].newSentence(count,sentence_score)
                    #For now, we'll just accept any key word
    def isSubject(self,dependancy):
        return spacy_tools.isDesiredWord(dependancy)
    def ScoreSentence(self,sentence):
        sentence = str(sentence.text)
        self.d.tokenize([sentence])
        self.d.predict()
        return self.d.results[0]

#this class is meant to track nouns or verbs
#that contribute to the overall emotion state
#of a person. Will probably only ever consist
#of a designation and an emotional weight
class SentimentTracker():
    def __init__(self, name = "Not named"):
        #there will probably be some encryption in this initialization function
        self.name =name
        self.ew = -1; #ew: emotion weight
        self.sentences = {}
        self.sentence_count = 0;
    def updateEmotionWeight(self, weight):
        self.ew = weight
    def newSentence(self, sentence_id,weight):
        self.sentence_count+=1
        self.sentences[sentence_id] = weight
    def calculateOverallSentiment(self):
        #calculates how the sentiment of the word evolves over the course of the document
        #this should probably be broken out so that the evolution can be explored over
        #each logged sentence. Because each sentence is ID'd with respect to the overall
        #document this shouldn't be hard. For now it is just a simple average.
        #This is one of the many examples of hand-wavy statistics that will need to be polished
        #through rigorous research and model training
        score_list = list(self.sentences.values())
        #take mean of each data point in 64-dof emotion space
        self.avg = np.mean(score_list,axis = 0)
    def to_json(self):
        jdict = {
            "name" : self.name,
            "sentences":list(self.sentences.keys()),
            "score" : spacy_tools.rawScoreToEmojis(self.avg)
        }
        return jdict

#I don't think we need to redefine the SentimentTracker as a class each time,
#But it may be that we just have to pass a few functions
