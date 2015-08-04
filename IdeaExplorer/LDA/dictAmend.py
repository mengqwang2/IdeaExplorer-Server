import os
import dataParse
import re
from collections import OrderedDict

def dictImport():
	dictlist=set()
	dp=dataParse.dataParse("../../data/ideas.txt")
	des=dp.fieldParse("tags")
	for d in des:
		d=re.sub(r'\W+', ' ', d)
		wordList=d.split(' ')
		for w in wordList:
			if(w):
				if(w!=' '):
					dictlist.add(unicode(w).encode('utf-8'))

	with open("dictnostops.txt","r") as fo:
		for line in fo:
			dictlist.add(line[:-1])

	dictNonReplicList=set()

	for wd in dictlist:
		wd = wd.lower()
		wd = re.sub(r'\W+', '', wd)
		dictNonReplicList.add(wd)
		#print wd
	
	#print dictNonReplicList
	fo=open("dictnostops.txt","w+")
	
	for ele in dictNonReplicList:
		fo.write(ele+"\n")

	fo.close()

if __name__=="__main__":
	dictlist=OrderedDict()
	with open("ideasVocab.txt","r") as fo:
		for line in fo:
			wd=line[:-1].lower()
			wd = re.sub(r'\W+', '', wd)
			dictlist.update({wd:1})
	fo.close()

	with open("dictnostops.txt","r") as fo:
		for line in fo:
			wd=line[:-1].lower()
			wd = re.sub(r'\W+', '', wd)
			dictlist.update({wd:1})

	fo.close()

	fo=open("vocabulary.txt","w+")
	
	for k in sorted(dictlist):
		fo.write(k+"\n")

	fo.close()