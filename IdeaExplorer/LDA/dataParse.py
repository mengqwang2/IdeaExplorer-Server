import jsonParser

class dataParse():
    def __init__(self,fp):
        self.__jp=jsonParser.jsonParser(fp)
        self.__filePath=fp
        self.__jp.parse()
        self.__ideas=self.__jp.getJsonDict()


    def fieldParse(self,fname):
        docDict=dict()
        for ind in self.__ideas['data']:
            docDict[ind['id']]=ind[fname]
        return docDict


    def concatedField(self,fList):
        fieldList=[]
        with open(fList) as fo:
            for line in fo:
                fieldList.append(line)
        docList=[]
        indexList=[]
        doc=""
        for ind in self.__ideas['data']:
            doc=""
            for fl in fieldList:
                fl=fl[:-1]
                if(ind[fl]==None):
                    doc=doc+"\n"
                else:
                    doc=doc+ind[fl]+"\n"
            docList.append(doc)
            indexList.append(ind["id"])

        return (docList,indexList)



