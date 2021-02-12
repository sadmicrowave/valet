###########################################################################
#
## @file intelligence.py
#
###########################################################################

import os, sys, re, pickle, json, random

#from multiprocessing import Queue

from ..io.language import Language
from .train import Train
from .ability import Ability

###########################################################################

class Intelligence :
	"""###########################################################################
	
	A wrapper for Valet to gather and learn responses with advanced scheduled
	jobs which iterate over learned data & previous responses/sites to 
	continue building a response library overtime.  This class is also used
	to determine which type of response to provide and the sequence that
	should be executed in determine the appropriate response.  
	
	TO DO
	1. Intelligence should have a lookup mechanism / sequence 
		\ internal response > db lookup > wikipedia > wolframalpha
	
	###########################################################################
	"""	
	#######################################################################
    #
    ##	Class level variables
    #
    #######################################################################
	model 		= None
	listen		= True
	
	
	def __init__ ( self, valet, ) :
		"""#######################################################################
    
    	Initialize the class accepting valet as the main object
    
    	@valet	/ instance of valet itself to interact with main object
    
	    #######################################################################
	    """
		    
		_ 	= self.__configure ( valet, )
		
		#_ 	= self.load ( )
	
	
	
	def process ( self, input, ) -> bool :
		"""#######################################################################
	    
    	Process is the main decision point within Valet's intelligence to
    	determine what to do with input - look up Ability from db, 
    	check against learned model, or lookup answer from search
    	ability where search sources will be used
    
		@input	/ str > the raw input string from the user
		Returns / bool > signifying completion
	    
	    #######################################################################
		"""
		###################################################################
		#
		##	Attempt to lookup input within 
		#	table to retrieve the available abililty - if found, and execute 
		#	it. For this we create and use the Ability base class which has a 
		#	location method to find classes from their path & name.
		#	All Ability methods are handled and executed internally
		#	within the Ability init for containment.	
		#
		###################################################################
		abilities = self.ability.search ( input, )

		if abilities  :		
	
			for ability in abilities :
	
				self.valet.server.pipeline.put_nowait ( abilities, )
			
				
			#self.valet.communicate.say ( 	'Certainly Sir,',
			#								self.valet.server.pipeline.get ( )
			#								#self.ability.execute_found_abilities ( abilities, )
			#							 )
															
		###############################################################
		#	If an ability was not found from a db lookup of skills

		#elif not self.valet.ability.found :
		#	
		#	pass
				
		else :
		
			self.valet.communicate.say ( "I'm sorry Sir, I'm not sure how to handle that request.", )

		
		return True
 
	
	def train ( self, ) -> bool :
		"""#######################################################################
	    
    	Train ensures explicit call for training allowing for easy off/on -
    	
    	Returns / bool > signifying completion
	    
	    #######################################################################
		"""
		
		self.valet.log.info ( ".training [ starting... ] \\\\" )

		self.valet.Train = Train ( valet=valet )
		
		self.valet.Train.trainer ( ).normalizer ( )
		
		# Close / compress the contents of trained.__compressbuffer__
		# trainingset = 'trainingset-%s.tar.gz' % ( datetime.datetime.now().strftime ( "%Y%m%d%H%M%S" ) )
		# tar = tar ( os.path.join ( self.valet.Train.trained_store, '__compressbuffer__', '*' ),
		#			  os.path.join ( self.valet.Train.trained_store, '%s' % trainingset )
		# 
		# Empty compressbuffer to prevent compressing in next batch
		# for f in glob.glob ( os.path.join ( self.valet.Train.trained_store, '__compressbuffer__' ) ) :
		#	os.remove ( f )
		
		self.valet.log.info ( ".training [ complete. ] \\\\" )
		
		return True
	
	
		
	def save ( self, ) -> bool :
		"""#######################################################################
    
    	Memory loads the intelligence cube or Valet's memory from the 
    	defined memory file
    	
    	Returns / bool > signifying completion
    
	    #######################################################################
		"""	
		#self.valet.Language.model.save ( self.model_path, save_format='h5' )

		self.valet.log.info ( '.memory [ successfully saved. ] \\\\' )
		
		return True
		
		
	
	def load ( self, ) -> bool :
		"""#######################################################################
    
    	Memory loads the intelligence cube or Valet's memory from the 
    	defined memory file
    	
    	Returns / bool > signifying completion
    
	    #######################################################################
	    """	
		#self.valet.Language.model 	= keras.models.load_model ( self.model_path )
		#self.valet.Language.intents	= self.__load_intents ( )
		
# 		self.vocabulary = pickle.load ( open ( self.intel_cube, 'rb' ) )
# 		
# 		self.vectorizer = TfidfVectorizer ( 
# 									tokenizer		= self.__normalize, 
# 									vocabulary		= self.vocabulary,
# 									token_pattern	= None,
# 									decode_error	= 'replace',
# 									max_features	= 20000, 
# 									strip_accents	= 'unicode',
# 									stop_words		= None, #stopwords,
# 									analyzer		= 'word', 
# 									use_idf			= True,
# 									ngram_range		= (1,2),
# 									sublinear_tf	= True,
# 									norm			= 'l2'
# 								)
		self.valet.log.info ( '.memory [ successfully loaded. ] \\\\' )
		
		return True
		
		
		
	def __load_intents ( self, path, ) :
		"""#######################################################################
	    
    	loads specifically the intents file for querying and identifying
    	intents from the prediction model
    
    	@path	/ str > string containing the path of the file to open
    
	    #######################################################################
	    """
		
		return json.loads ( open ( path ).read( ) )



	def __load_vocabulary ( self, path, ) :
		"""#######################################################################
    
    	Load vocabulary loads the vocabulary file containing the words to
    	attempt matching against and for pattern recognition
    
    	@path	/ str > string containing the path of the file to open
    
	    #######################################################################
	    """
	    
		return pickle.load ( open ( path, 'rb' ) )

	
	def __configure ( self, valet, ) -> bool :
		"""#######################################################################
	    
    	Perform any setup needed for tokenizer or Intelligence to do it's
    	job.  Here the data set reader for deep pavlov needs to be set to
    	read from the normalized path.  Because ODQA model uses 
    	en_ranker_tfidf_wiki as a ranker, we can load its config separately, 
    	and substitute data_path that is uses for training.
    	Also, decrease the batch size here, otherwise the training process 
    	will not fit into memory.
    
    	@valet	/ instance of valet itself to interact with main object
    	Returns / bool > signifying completion
		
	    #######################################################################"
		"""
		
		self.valet 				= valet
		self.store  			= valet.ini.pool['intelligence']['structure']['store']
		self.model_path	 		= os.path.join ( self.store, valet.ini.pool['intelligence']['structure']['model'] )
		self.untrained_store 	= os.path.join ( self.store, 'untrained' )
		self.trained_store 		= os.path.join ( self.store, 'trained' )

		###################################################################
		#
		## 	Instantiate the language helper which loads the Natual Language
		#	Tool Kit for NLP and provides methods to interact with parts of
		#	speech
		#
		###################################################################
		self.valet.Language	 	= Language ( valet, )


		#_config 									= read_json(configs.doc_retrieval.en_ranker_tfidf_wiki)
		#_config["dataset_reader"]["data_path"] 		=  os.path.join ( self.untrained_store, '__normalize__' )
		#_config['dataset_reader']['dataset_format'] = 'text'
		#_config['train']['batch_size'] 				= 1000
		#
		#_odqaconfig 													 = read_json ( configs.odqa.en_odqa_infer_wiki )
		#_odqaconfig['chainer']['pipe'][-1]['squad_model']['config_path'] = '{CONFIGS_PATH}/squad/squad_bert_infer.json'
	
		
		###################################################################
		#
		##	Ability Engine needs to be initiated here for intelligence
		#	and core processor to utilize during input lookup
		#
		###################################################################
		self.ability	 		= Ability ( valet, )


		return True

