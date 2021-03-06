import numpy
import dataParse
import onlineldavb
import os


class IdeaLDA():
    def __init__(self,batchsize,d,k,tau,kappa):
        self.__dp=dataParse.dataParse(os.path.abspath("./data/ideas.txt"))
        self.__result=self.__dp.concatedField(os.path.abspath("./data/fieldList.txt"))
        #doc
        self.__doc=self.__result[0]
        #fielddata
        self.__fid=self.__result[1]
        #dictionary
        self.__vocab=file(os.path.abspath('./data/vocabulary.txt')).readlines()
        # the number of words in the dictionary
        self.__W=len(self.__vocab)
        #the number of documents to analyze in each iteration
        self.__batchsize=batchsize
        # the total number of documents
        self.__D=d
        # the number of topics
        self.__K=k
        # the number of iterations
        self.__documentstoanalyze=self.__D/self.__batchsize
        # tau
        self.__tau=tau
        # kappa
        self.__kappa=kappa
        # lda instance (alpha=1/K, eta=1/K, tau_0=1024, kappa=0.1)
        self.__ldaObj=onlineldavb.OnlineLDA(self.__vocab, self.__K, self.__D, 1./self.__K, 1./self.__K, self.__tau*1.0, self.__kappa)


    def runLDA(self):
        for iteration in range(0, self.__documentstoanalyze):
            #Retrieve texts
            docset=self.__doc[iteration*self.__batchsize:iteration*self.__batchsize+self.__batchsize]

            # Give them to online LDA
            (gamma, bound) = self.__ldaObj.update_lambda(docset)


            # Compute an estimate of held-out perplexity
            (wordids, wordcts) = onlineldavb.parse_doc_list(docset, self.__ldaObj._vocab)
            perwordbound = bound * len(docset) / (self.__documentstoanalyze * sum(map(sum, wordcts)))
            print '%d:  rho_t = %f,  held-out perplexity estimate = %f' % \
            (iteration, self.__ldaObj._rhot, numpy.exp(-perwordbound))


            # Save a temporary lambda for this iteration
            temp_lambda = self.__ldaObj._lambda

            # Save lambda and gamma
            if (iteration == 0):
                self.__lambda_all = temp_lambda
            else:
                self.__lambda_all = numpy.concatenate((self.__lambda_all,temp_lambda), axis=0)

            if (iteration == 0):
                self.__gamma_all = gamma
            else:
                self.__gamma_all = numpy.concatenate((self.__gamma_all,gamma), axis=0)

            numpy.savetxt('./data/lambda.dat', self.__lambda_all)
            numpy.savetxt('./data/gamma.dat', self.__gamma_all)

