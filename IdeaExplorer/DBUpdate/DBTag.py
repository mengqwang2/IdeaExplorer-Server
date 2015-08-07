import os,sys

class DBTag():
	def doctag(self):
		doc_tag_list=dict()
		with open("../data/tag.txt","r+") as f:
			for line in f:
				tagList=line.split()
				if tagList[0] not in doc_tag_list:
					doc_tag_list[tagList[0]]=[]
				for ele in tagList[1:]:
					doc_tag_list[tagList[0]].append(ele)

		return doc_tag_list


	def tagdoc(self):
		tag_doc_list=dict()
		with open("../data/tag.txt","r+") as f:
			for line in f:
				doc_tag=line.split()
				for tag1 in doc_tag[1:]:
					if tag1 not in tag_doc_list:
						tag_doc_list[tag1]=[]
					tag_doc_list[tag1].append(doc_tag[0])

		return tag_doc_list

