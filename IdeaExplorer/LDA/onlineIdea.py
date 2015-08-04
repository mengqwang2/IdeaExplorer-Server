import cPickle, string, numpy, getopt, sys, random, time, re, pprint
import dataParse
import onlineldavb
import wikirandom

def main():
    """
    Downloads and analyzes a bunch of random Wikipedia articles using
    online VB for LDA.
    """
    dp=dataParse.dataParse("../../data/ideas.txt")

    #des=dp.fieldParse("description")
    result=dp.concatedField("../../data/fieldList.txt")
    des=result[0]
    fid=result[1]
    

    # The number of documents to analyze each iteration
    batchsize = 100
    # The total number of documents in Wikipedia
    D = 5000
    # The number of topics
    K = 50

    # How many documents to look at
    if (len(sys.argv) < 2):
        documentstoanalyze = int(D/batchsize)
    else:
        documentstoanalyze = int(sys.argv[1])

    # Our vocabulary
    vocab = file('vocabulary.txt').readlines()
    W = len(vocab)
    #print W


    # Initialize the algorithm with alpha=1/K, eta=1/K, tau_0=1024, kappa=0.7
    olda = onlineldavb.OnlineLDA(vocab, K, D, 1./K, 1./K, 1024., 0.1)
    # Run until we've seen D documents. (Feel free to interrupt *much*
    # sooner than this.)
    for iteration in range(0, documentstoanalyze):
        #Retrieve texts
        docset=des[iteration*batchsize:iteration*batchsize+batchsize]
        # Give them to online LDA
        
        (gamma, bound) = olda.update_lambda(docset)
        # Compute an estimate of held-out perplexity
        (wordids, wordcts) = onlineldavb.parse_doc_list(docset, olda._vocab)
        perwordbound = bound * len(docset) / (D * sum(map(sum, wordcts)))
        print '%d:  rho_t = %f,  held-out perplexity estimate = %f' % \
            (iteration, olda._rhot, numpy.exp(-perwordbound))

        # Save lambda, the parameters to the variational distributions
        # over topics, and gamma, the parameters to the variational
        # distributions over topic weights for the articles analyzed in
        # the last iteration.
        
        numpy.savetxt('../../data/LDAResult/lambda-%d.dat' % iteration, olda._lambda)

        f=open("../../data/LDAResult/gamma"+str(iteration)+".dat","w+")
        st=iteration*batchsize
        for line in gamma:
            f.write(str(fid[st]))
            for ele in line:
                f.write(" "+str(ele))
            st=st+1
            
            f.write("\n")


        f.close()
    
    
if __name__ == '__main__':
    main()
