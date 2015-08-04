# Generate document files from raw ideas files

import sys,os
import dataParse

if __name__=="__main__":
	dp=dataParse.dataParse("../../data/ideas.txt")

	docSet=dp.concatedField("../../data/fieldList.txt")

	'''
	i=1
	for ele in docSet:
		fo=open("../../data/document/"+str(i)+".txt","w+")
		fo.write(unicode(ele).encode('utf-8'))
		i=i+1

	fo.close()
	'''

	fi=open("../../data/document/all.txt","w+")
	for ele in docSet:
		fi.write(unicode(ele).encode('utf-8'))

	fi.close()

