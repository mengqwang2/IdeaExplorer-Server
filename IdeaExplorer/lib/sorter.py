from operator import itemgetter
from collections import deque

class Sorter():
    def __init__(self,sorter,dlist):
        self.__sorter=sorter
        self.__dlist=dlist

    def doSort(self):
        if(self.__sorter=="relevance"):
            pass
        elif(self.__sorter=="upload_date"):
            self.__dlist=sorted(self.__dlist,reverse=True)

        elif(self.__sorter=="rating"):
            dataDict=dict()
            up=UserPost.objects.all()
            for upObj in up:
                if(upObj.docid in self.__dlist):
                    dataDict[upObj.docid]=upObj.avgrate

            for ele in self.__dlist:
                if ele not in dataDict:
                    dataDict[ele]=0
            data_sorted=[]

            dataDict_sorted=sorted(dataDict.iteritems(),key=itemgetter(1),reverse=True)

            for ele in dataDict_sorted:
                data_sorted.append(ele[0])
            self.__dlist=data_sorted


        elif(self.__sorter=="no_comments"):
            dataDict=dict()
            up=UserPost.objects.all()

            for upObj in up:
                if(upObj.docid in self.__dlist):
                    dataDict[upObj.docid]=len(upObj.comments)

            for ele in self.__dlist:
                if ele not in dataDict:
                    dataDict[ele]=0

            data_sorted=[]
            dataDict_sorted=sorted(dataDict.iteritems(),key=itemgetter(1),reverse=True)
            for ele in dataDict_sorted:
                data_sorted.append(ele[0])
            self.__dlist=data_sorted


    def getList(self):
        return self.__dlist
