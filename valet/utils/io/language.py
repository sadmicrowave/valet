###########################################################################
#
## @file language.py
#
###########################################################################

import os, sys, re, requests, datetime, random, string, unicodedata

import nltk, numpy

#from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
#from collections import defaultdict
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.metrics.pairwise import cosine_similarity, linear_kernel  

###########################################################################

class Language :
	"""###########################################################################
	
	A wrapper for Valet to normalize text entry for language processing
	
	###########################################################################
	"""	
	#######################################################################
    #
    ##	Class level variables
    #
    #######################################################################
	vocabulary = None
	
	
	
	def __init__ ( self, valet, ) :
		"""#######################################################################
	    
    	Initialize the class accepting valet as the main object
    
    	@valet	/ instance of valet itself to interact with main object
    
		#######################################################################
		"""	
		_ 		= self.__configure ( valet, )
		
		
		
		
	
	def __predict_class ( self, input, ERROR_THRESHOLD=0.25, ) :
		"""#######################################################################
	    
    	Predict Class we use an error threshold of 0.25 to avoid too much 
    	overfitting. This function will output a list of intents and the 
    	probabilities, their likelihood of matching the correct intent. 
    
    	@input 	/ str > sentence string to base predictions upon
    	Returns : sentences list
    
	    #######################################################################
	    """
    	
		return_list = []
		
		# filter out predictions below a threshold
		p = self.normalize ( input, self.words, )
		
		res = self.model.predict ( numpy.array ( [p] ) )[0]
		
		results = [ [i,r] for i, r in enumerate ( res ) if r > ERROR_THRESHOLD ]
		
		# sort by strength of probability
		results.sort ( key=lambda x: x[1], reverse=True )
		
		for r in results :
			
			return_list.append ( {	"intent" 		: classes[ r[0] ], 
									"probability"	: str ( r[1] ) 
								  }
								)
		
		return return_list

	
	
	def normalize ( self, input, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', ) :
		"""#######################################################################
	    
    	Normalization is a process that converts a list of words to a more 
    	uniform sequence. This is useful in preparing the text for later 
		processing. By transforming the words to a standard format, other 
    	operations are able to work with the data and will not have to deal 
    	with issues that might compromise the process.
		This step involves word tokenization, Removing ASCII values, Removing 
		tags of any kind, Part-of-speech tagging, and Lemmatization. 
    
    	@input	/ str > input string to tokenize into sentences 
    	Returns : sentences list
    
	    #######################################################################
		"""
		lemmatizer = WordNetLammatizer ()

		# tokenize the pattern
		sentence_words = nltk.word_tokenize ( input )
		sentence_words = [ lemmatizer.lemmatize ( word.lower ( ) ) for word in sentence_words ]
	
		# bag of words - matrix of N words, vocabulary matrix
		bag = [0] * len ( self.vocabulary )
		for sentence in sentence_words :
	
			for i, word in enumerate ( self.vocabulary ) :
				
				# assign 1 if current word is in the vocabulary position
				if word == sentence :
					bag [ i ] = 1
				
					#if self.valet.verbose :	
					#	print ("found in bag: %s" % w)
			
		return ( numpy.array( bag ) )


		
	
	def __configure ( self, valet, ) -> bool :
		"""#######################################################################
	    
    	Perform any setup needed for tokenizer or Intelligence to do it's
    	job
    
    	@valet	/ instance of valet itself to interact with main object
    	@Returns / bool signifying completion
	
	    #######################################################################
		"""		
		self.valet = valet

		libraries = [	'tokenizers/punkt', 
						'corpora/wordnet',
						'taggers/averaged_perceptron_tagger'
					]
		
		for library in libraries :
		
			try :
			
				nltk.data.find ( library )
			
			except LookupError :
			
				nltk.download ( library.split ( '/' )[-1:] )
		
		return True
		
		
		
		
		
		
		
		
		
# 	def __normalize ( self, text ) :
# 		
# 		remove_punct_dict = dict( ( ord( punct ), None ) for punct in string.punctuation )
# 		
# 		#word tokenization
# 		word_token = nltk.word_tokenize ( text.translate ( remove_punct_dict ) )
# 		
# 		#remove ascii
# 		new_words = [ ]
# 		for word in word_token :
# 		
# 			new_word = unicodedata.normalize ( "NFKD", word ).encode( 'ascii', 'ignore' ).decode ( 'utf-8', 'ignore' )
# 			new_words.append ( new_word )
# 		
# 		#Remove tags
# 		rmv = [ ]
# 		for w in new_words :
# 		
# 			#text = re.sub( "&lt;/?.*?&gt;","&lt;&gt;", w )
# 			text = re.compile( r"<([^>]+)>", flags=re.UNICODE ).sub( "", text )
# 
# 			rmv.append( text )
# 		    
# 		#Part of Speech tagging and lemmatization
# 		tag_map = defaultdict( lambda : wn.NOUN )
# 		tag_map['J'] = wn.ADJ
# 		tag_map['V'] = wn.VERB
# 		tag_map['R'] = wn.ADV
# 		lmtzr = WordNetLemmatizer ( )
# 		lemma_list = [ ]
# 		rmv = [ i for i in rmv if i ]
# 	
# 		for token, tag in nltk.pos_tag ( rmv ) :
# 	
# 			lemma = lmtzr.lemmatize ( token, tag_map [ tag [ 0 ] ] )
# 			lemma_list.append ( lemma )
# 	
# 		return lemma_list
		
		

		