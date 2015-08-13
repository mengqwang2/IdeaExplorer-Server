import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import models
from models import *
import DBGamma,DBLambda,DBSim,DBTag,DBVocab

class DBGen():
	def DBMain(self):
		#Update table <GammaTD>, <GammaDT>
		gammaObj=DBGamma.DBGamma("../data/gamma.dat")
        d1=gammaObj.gammaDT()
        d2=gammaObj.gammaTD()

        for k,v in d1.iteritems():
            go=GammaDT()
            go.docid=k
            go.gamma=v
            go.save()

        for k,v in d2.iteritems():
            go=GammaTD()
            go.topicid=k
            for k1,v1 in v.iteritems():
                dg=DocGamma()
                dg.docid=k1
                dg.gamma=v1
                go.gam.append(dg)
            go.save()
        
        #Update table <LambdaWT>, <LambdaTW>
        lamObj=DBLambda.DBLambda("../data/lambda.dat")
        d1=lamObj.lam_tw()
        d2=lamObj.lam_wt()
        for k,v in d2.iteritems():
            ld=LambdaWT()
            ld.wordid=k
            ld.lam=v
            ld.save()
        
        for k,v in d1.iteritems():
            ld=LambdaTW()
            ld.topicid=k
            ld.lam=v
            ld.save()
        
        gammaObj=Gamma.objects.all()
        #print gammaObj
        
        gammaDict=dict()
        for g in gammaObj:
            gammaDict[g.docid]=g.gamma

        
        #Update table <DocSim>, <Similarity>
        sim=DBSim.DBSim(gammaDict)
        simResult=sim.similarity()
        
        for k,v in simResult.iteritems():
            docsimObj=DocSim()
            docsimObj.docid=int(k)
            for k1,v1 in v.iteritems():
                simObj=Similarity()
                simObj.docid=int(k1)
                simObj.sim=float(v1)
                docsimObj.similarity.append(simObj)
            docsimObj.save()
        
        
        #Update table <Vocab>
        dv=DBVocab.DBVocab("../data/vocabulary.txt")
        vocList=dv.vocabBuilder()
        ind=0
        for ele in vocList:
            vocObj=Vocab()
            vocObj.vid=ind
            vocObj.word=ele
            vocObj.save()
            ind=ind+1

        #Update table <DocTag>, <TagDoc>
        dt=DBTag.DBTag()
        doc_tag_list=dt.doctag()
        for k,v in doc_tag_list.iteritems():
        	dtObj=DocTag()
        	dtObj.docid=int(k)
        	dtObj.tags=v
        	dtObj.save()

        tag_doc_list=dt.tagdoc()
        for k,v in tag_doc_list.iteritems():
        	tdObj=TagDoc()
        	tdObj.tag=k
        	tdObj.docid=v
        	tdObj.save()




