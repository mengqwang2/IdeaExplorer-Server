import io, json

class JsonValidator():
	def __init__(self,fp):
		self.__fp=fp
		with open("../data/ideas.txt") as json_file:
			self.__data=json.load(json_file,strict=False)

	def doUnicode(self):
		with io.open("../data/ideas_utf8.txt", 'w', encoding='utf-8') as f:
			f.write(unicode(json.dumps(self.__data, ensure_ascii=False)))
