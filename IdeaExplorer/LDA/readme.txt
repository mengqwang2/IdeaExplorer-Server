# onlineldavb is copied from Internet for implementing LDA algorithm. It is written by Matthew D. Hoffman.
# dataParse and jsonParser is to read and separate ideas.txt into the input format.
# jsonValidator is written in case that Python can not read the encoding format for some characters.
# Run onlineIdea and tagGen to get lambda, gamma, tag set respectively, which are stored in data file. Field list and vocabulary are provided.

# About the algorithm
## LDA is a unsupervised algorithm. So the performance cannot be judged directly.
## online LDA updates the result in each iteration.
## lambda is the parameters to the variational distributions over topics
## gamma is the parameters to the variational distributions over topic weights for the documents
## Some parameters could be adjusted to get a better result. Good parameter usually defers from the data set and is based on experience to choose.
## These parameters are topic numbers, batch size, tau and kappa.
## tau and kappa combines to effect rho_t, which is a parameter that determines the weight of the result in this training.
## 1000 topics are usually large enough, and the result will not differ much from 2000 topics. Here we use 100 topics.
## batch size should not be too large or small.
## rho_t goes smaller as the iteration increases.(i.e. the result of the previous iteration plays more weight)
## Increasing kappa and tau can decrease the value of rho_t.
## Perplexity is a reference for the performance of a result. Under the same condition, the smaller a perplexity is, the better the result is. It could be used to help to evaluate a result.
## For each tag , tag set stores the documents that contain this tag.

# Some other attention:
## Remember keep a blank line at the end of field list if you want to make any change.(It is added at present)
## Vocabulary could be modified manually to decrease some meaningless words to get better performance.
## The performance of this algorithm may differ from the size of data(i.e. the number of documents)
## In database, the similarity between every two documents are calculated based on gamma. We use the distance between gammas to represent similarity. The smaller the distance is, the larger the similarity is. The definition of distance here is Euclidean distance. Changing the definition of distance may lead to better result.
