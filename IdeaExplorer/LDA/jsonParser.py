import json

class jsonParser():
	def __init__(self,filePath):
		self.__js_data=dict()
		self.__fp=filePath

	def parse(self):
		with open(self.__fp) as json_file:
			self.__js_data=json.load(json_file,strict=False)

	def getJsonDict(self):
		return self.__js_data
