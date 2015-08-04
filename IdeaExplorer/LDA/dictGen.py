# Generate a dictionary / vocabulary from a text dataset.
import gensim
import nltk
import argparse
import codecs
#from nltk.tokenize import PunktWordTokenizer

argparser = argparse.ArgumentParser()
argparser.add_argument("dataset", type=str, help="Input dataset filename.")
argparser.add_argument("-o", "--outfile", dest="outfile", default='vocab.txt', help="Output filename. (default='vocab.txt')")
argparser.add_argument("-t", "--threshold", type=int, dest="threshold", default=20, help="Word count threshold; excludes words below threshold. (default=20)")
args = argparser.parse_args()

def generate(f, outfile, t):
	print "Tokenizing file."
	sentToks=nltk.tokenize.load('tokenizers/punkt/english.pickle')
	wordToks=nltk.tokenize.TreebankWordTokenizer()
	text=unicode(codecs.open(f).read(),'utf-8')
	sents = sentToks.tokenize(text)
	toks=[]

	for s in sents:
		toks.extend(wordToks.tokenize(s))

	
	print "Generating word counts."
	dictionary = gensim.corpora.dictionary.Dictionary([toks])
	#print dictionary
	bag_of_words = dictionary.doc2bow(toks)
	
	print "Filtering words with less than {0} occurrences.".format(t)
	good_ids = map(lambda y: y[0], filter(lambda x: x[1] > t, bag_of_words))
	dictionary.filter_tokens(bad_ids=None, good_ids=good_ids)
	
	print "Writing output to {0}.".format(outfile)
	with open(outfile, 'w') as of:
		for word in dictionary.values():
			of.write("{0}\n".format(unicode(word.lower()).encode('utf-8')))
	
	print "Done."
	
generate(args.dataset, args.outfile, args.threshold)