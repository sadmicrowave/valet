###########################################################################
#
## @file train.py
#
###########################################################################

import os, sys

import numpy

from deeppavlov import configs
from deeppavlov.core.commands.infer import build_model
from deeppavlov.core.common.file import read_json

#from keras.models import Sequential
#from keras.layers import Dense, Activation, Dropout
#from keras.optimizers import SGD

sys.path.append('..')
from abilities.taught.normalize import Normalize

###########################################################################

class Train :
	"""###########################################################################
	
	A wrapper for Valet to train the model for language processing
	
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
		_		= self.__configure ( valet )



	def trainer ( self, ) :
		"""#######################################################################
	    
    	Processor handles the main processing of the intelligence files, to
    	learn. Here the main intel_store is iterated and parsed into language
    	intelligence to be stored in the large language list(s)
    
    	Constraints: only look for source files that haven't been learned
    
	    #######################################################################
	    """		
		normalizer = Normalize ( self.valet, )

		###################################################################
		#
		#	Loop over files in unlearned store & normalize each into train-
		#	able text files for - excluding any file starting with . (hidden)
		#	files
		#
		###################################################################
		for fn in glob.glob ( '%s/[!.]*' % self.untrained_store, recursive=False ) :
			
			###########################################################
			#
			#	Use an unpacker method to determine the file type 
			#	and extract the components / text appropriately from
			#	each file / object
			#	> unpacks into __normalize__ directory
			#
			###########################################################
			#unpacked = self.__unpack ( filename )

			corpus = Open ( filename )
	
	
			normalized = normalizer.execute ( unpacked )
		
		
			
			###########################################################
		    #
		    ##	Move file to learned source intelligence directory
		    #
		    ###########################################################
			os.rename ( os.path.join ( self.untrained_store, filename ), 
						os.path.join ( self.trained_store, filename ) 
					)
					
	
	
	def train ( self,  ) :
		"""#######################################################################
	    
    	Train the input string into sentences and normalize for use
    
    	@filename 	/ str > file name
    	@input		/ str > input string to tokenize into setences 
    
	    #######################################################################
		"""
		_ 	= train_model ( self.modelconfig, download=False )
		
		print ( 'Successfully trained intelligence model.' )
		
		return
				
	
	
			
	def __configure ( self, valet, ) -> bool :
		"""#######################################################################
    
    	Perform any setup needed for the  class  to do its job.  
    
    	@valet	/ instance of valet itself to interact with main object
		Returns / bool > signifying completion
	
		#######################################################################
		"""
		
		self.valet 				= valet
		self.untrained_store 	= os.path.join ( self.valet.intelligence.store, 'untrained' )
		self.trained_store 		= os.path.join ( self.valet.intelligence.store, 'trained' )
		
		self.modelconfig 									 = read_json(configs.doc_retrieval.en_ranker_tfidf_wiki)
		self.modelconfig["dataset_reader"]["data_path"] 	 =  os.path.join ( self.untrained_store, '__normalize__' )
		self.modelconfig['dataset_reader']['dataset_format'] = 'text'
		self.modelconfig['train']['batch_size'] 			 = 1000
		
		self.odqaconfig 													 = read_json ( configs.odqa.en_odqa_infer_wiki )
		self.odqaconfig['chainer']['pipe'][-1]['squad_model']['config_path'] = '{CONFIGS_PATH}/squad/squad_bert_infer.json'
	
		return True
		
		
	
	#######################################################################
    #
    ##	Provide a vector analysis of the content to be added to the
    #	intelligence model - a preprocessing sanity check
    #
    #	@input	/ str > input string to tokenize into setences 
    #	Returns : sentences list
    #
    #######################################################################
	#def preanalyzer ( self, input, ) :
	#	
	#	self.tf.build_analyzer ( )( input )