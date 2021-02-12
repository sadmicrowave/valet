###########################################################################
#
## @file normalize.py
#
###########################################################################

import os, json

#from ..ability import Ability
from .open import Open
  
###########################################################################
#
##   A wrapper for Valet to convert contents of a file to raw text for 
#	 training and other iterative purposes - all internal methods should
#	 return raw text
#
###########################################################################


class Normalize :
	
	#######################################################################
    #
    ##	Class level variables
    #
    #######################################################################
	corpus		= None

	#######################################################################
    #
    ##	Instantiation of normalize ability, should take path and extract
    #	contents - ensuring raw text is returned 
    #
    #	@valet	/ instance of valet itself to interact with main object
    #	@input	/ str > filename / path to use in file opener
    #
    #######################################################################
	def __init__ ( self, valet, input=None, ) :
		
		self.input		 = input
		_				 = self.__configure ( valet )		
				
		
	#######################################################################
    #
    ##	Instance executor so the execution must be directly and intentionally
    #	called rather than calling upon instantiation.  Here, we split
    #	out operations depending on what the learning resource type is.	
    #
    #	@filepath > str / string providing specific filename pointer to open
    #	@pattern > str / dictactes the normalization pattern to use
    #	@corpus > str / string to normalize if provided instead of file
	#	Returns: text object from file
	#
    #######################################################################
	def execute ( self, filepath=None, pattern=None, corpus=None, ) :
		
		
		if filepath and not pattern :
			# Get pattern from filepath (the extension of the file name)
			pattern = os.path.splitext ( filepath )[1][1:]
	
	
		###################################################################
		#
		##	Attempt the lookup of the extension within the defined handlers
		#	if it idesn't exist handle the exception gracefully
		#
		###################################################################
		try :
				
			return handlers [ pattern ] ( corpus )
		
		except KeyError as e :
		
			print ( 'No normalization method found for `%s` file types.  Skipping.' % extension )
			
			pass
	
	
	

	#######################################################################
    #
    ##	normalize_json is used to extract the contents of json files and
    #	look for specific contexts to extract as text to train
    #
    #	@input 	/ str > input string to parse into json object and extract
    #	Returns : string of compiled contents from json search components
    #
    #######################################################################
	def __normalize_json ( self, input, _corpus='', ) :
			
		decoded = json.load ( input )
		###################################################################
		#
		# Search the content for any of the context types below and extract
		# the text from the dictionary attribute if it exists
		#
		###################################################################		
		for context in ['abstract', 'body_text'] :
		
			try :
				
				_corpus.append ( ' '.join ( [ x[ 'text' ] for x in decoded[ context ] ] ) )
				
			except KeyError as e :
				
				continue 
		
		return _corpus




	#######################################################################
    #
    ##	Perform any setup needed for the  class  to do it's job.  
    #
    #	@valet	/ instance of valet itself to interact with main object
	#
    #######################################################################
	def __configure ( self, valet, ) :

		self.valet		= valet
		self.handlers 	= { 'json' 	: self.__normalize_json
							}
													
		return 
