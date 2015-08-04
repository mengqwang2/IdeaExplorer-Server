import dataParse
import numpy
import os,sys

class TagGen():
    def __init__(self,docNum,fp):
        self.__dp=dataParse.dataParse(fp)
        self.__docNum=docNum
        self.__tags=self.__dp.fieldParse("tags")
        
    def wordTrim(self,word):
        punc = ["(", ")", ":", ";", ",", "-", "!", ".", "?", "/", "\"", "*","#","_","@"]
        word = word.lower()
        for p in punc:
            word=word.replace(p, " ")
            wordlist=word.split()
            print wordlist
            wordlist=list(set(wordlist))
        return " ".join(wordlist)

    def generateAllTags(self):
        f2 = open("../../data/tag.txt","w+")
        for k,v in self.__tags.iteritems():
            if v=="":
                v="na"
            word = unicode(v).encode('utf-8')
            word1 = self.wordTrim(word)
            f2.write(str(k)+" "+word1+'\n')
        f2.close()
    


