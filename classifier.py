"""
java -mx1000m -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -loadClassifier classifiers/english.all.3class.distsim.crf.ser.gz -port 8888 -outputFormat inlineXML
"""
import subprocess
import ner
import sys
import os
import time
       
from nltk.tag import StanfordNERTagger


tagger = None

def start_classifier():
    global tagger
    tagger = ner.SocketNER(host='localhost', port=8888)




def tag(text, org_filter=None):
    global tagger
    
    tagged = []

    if not text:
        return tagged

    if type(text) is list:
        text = " ".join(text)
    
    if not tagger:
        start_classifier()

    classified_text = tagger.get_entities(text)

    return classified_text
