import json
import emoji
import numpy as np

emoji_dict = {
    "0":":joy:",
    "1":":unamused:",
    "2":":weary:",
    "3":":sob:",
    "4":":heart_eyes:",
    "5":":pensive:",
    "6":":ok_hand:",
    "7":":blush:",
    "8":":heart:",
    "9":":smirk:",
    "10":":grin:",
    "11":":notes:",
    "12":":flushed:",
    "13":":100:",
    "14":":sleeping:",
    "15":":relieved:",
    "16":":relaxed:",
    "17":":raised_hands:",
    "18":":two_hearts:",
    "19":":expressionless:",
    "20":":sweat_smile:",
    "21":":pray:",
    "22":":confused:",
    "23":":kissing_heart:",
    "24":":heart:",
    "25":":neutral_face:",
    "26":":information_desk_person:",
    "27":":disappointed:",
    "28":":see_no_evil:",
    "29":":weary:",
    "30":":v:",
    "31":":sunglasses:",
    "32":":rage:",
    "33":":thumbsup:",
    "34":":cry:",
    "35":":sleepy:",
    "36":":yum:",
    "37":":triumph:",
    "38":":hand:",
    "39":":mask:",
    "40":":clap:",
    "41":":eyes:",
    "42":":gun:",
    "43":":persevere:",
    "44":":smiling_imp:",
    "45":":sweat:",
    "46":":broken_heart:",
    "47":":green_heart:",
    "48":":musical_note:",
    "49":":speak_no_evil:",
    "50":":wink:",
    "51":":skull:",
    "52":":confounded:",
    "53":":smile:",
    "54":":stuck_out_tongue_winking_eye:",
    "55":":angry:",
    "56":":no_good:",
    "57":":muscle:",
    "58":":punch:",
    "59":":purple_heart:",
    "60":":sparkling_heart:",
    "61":":blue_heart:",
    "62":":grimacing:",
    "63":":sparkles:"
}

#these functions are meant to help if a spacy token
#is in fact what we're looking for
def top_elements(array, k):
    ind = np.argpartition(array, -k)[-k:]
    return ind[np.argsort(array[ind])][::-1]

def rawScoreToEmojis(scores):
    top_scores = top_elements(scores,5)
    print(top_scores)
    return [emoji.emojize(emoji_dict[str(score)]) for score in top_scores]

def isDesiredWord(dep):
    desired_dependencies = ['ROOT','nsubj','dobj']
    if dep in desired_dependencies:
        return True
    return False

def isEntity(dep):
    desired_dependencies = ['nsubj','dobj']
    if dep in desired_dependencies:
        return True
    return False

def isAct(dep):
    desired_dependencies = ['ROOT']
    if dep in desired_dependencies:
        return True
    return False

def handlePRONs(token):
    personal_pronouns = ["I","me"]
    if token in personal_pronouns:
        return "I"
    else:
        return "unregistered pronoun"

#this function makes sure a lemma that
#we want is useful.
def getLemma(token):
    #handle the special case that if it's
    #a pronoun, then we figure out how to
    #make sure it is accounted for properly
    if token.lemma_ =='-PRON-':
        lemma = handlePRONs(token.text)
        return lemma
    return token.lemma_
