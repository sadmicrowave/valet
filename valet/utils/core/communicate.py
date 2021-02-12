###########################################################################
#
## @file communicate.py
#
###########################################################################

import os, sys, textwrap, subprocess, queue

from . import communicate_pb2_grpc


#from collections.abc import Iterable

from ..canonical.colors import Colors
from ..io.speech.speak import Speak
from ..io.speech.fragments.greeting import Greeting
from ..io.speech.fragments.salutation import Salutation


class Communicate :
	"""###########################################################################
	
	A wrapper for Valet to communicate with written or vocalized speech
	providing one callable class which handles the delegation of output
	context through cli and other i/o registered devices
	
	###########################################################################
	"""

	#######################################################################
    #
    ##	Class level variables
    #
    #######################################################################
	formatted_output 	= None
	listen				= True
	colors				= Colors

	
	###################################################################
	#
	##	Set the parts of speech modules accessible to Valet, allowing
	#	accessors from the main valet.py to import Speech without 
	#	directly importing all parts of speech
	#
	###################################################################
	greeting	= Greeting ( )
	salutation	= Salutation ( )
	
	
	def __init__ ( self, valet=None, grpcserver=None, communicationservicer=None, ) :
		"""#######################################################################
	    
    	Initialize communication manager to handle and interact with
    	calls for output and inputs.
    
    	@valet	/ instance of valet itself to interact with main object
	    
	    #######################################################################
		"""	
		
		_ 		= self.__configure ( valet, grpcserver, )



	def say ( self, *args, ) -> bool :
		"""#######################################################################
	
		Say provides an additional wrapper to invoke both cli write &
		vocalized speech with .vocalize - only if vocalization is enabled
		within the config file main.  Processes list of strings to output
		or single string (which gets put into a list)
	
		*args / str|list > string or list of values to print as output 
			  / from Valet - passed as multiple arguments or single arg
			  / list
		
	    #######################################################################
		"""
			
		for arg in args or ( ) :
			
			item = arg
			
			# Make item into a Queue type if not already
			if not isinstance ( item, Queue, ) : 
			
				item = queue.Queue ( )
				item.put ( arg )
			
			while not item.empty ( ) :
			
				_current = item.get_nowait ( )
				 
				if self.speak.enabled :	
				
					self.speak.vocalize ( _current, )		
				
				self.__write ( _current, )
				
		
		return True
				
				
				
	def __write ( self, output, _console=None, ) -> bool :
		"""#######################################################################
	
		Write the provided output to the provided / configured device
		output - this is a print wrapper
	
		@output / str > string value to print as output from Valet
		Returns / bool > signifying completion
	
	    #######################################################################
		"""
			
		( _console or self.console ).fill ( 
			
			'%s %s%s' % ( self.colors.OKBLUE, output, self.colors.ENDC )
		)
	
		return True



	def __configure ( self, valet=None, grpcserver=None, communicationservicer=None, ) -> bool :
		"""#######################################################################
    
    	Perform any setup needed for the  class  to do its job.  
    
    	@valet	/ instance of valet itself to interact with main object
    	@grpcserver	/ grpc instance > protobuf server instance for thread management
		Returns / bool > signifying completion
	
		#######################################################################
		"""
		self.valet 			= valet
		
		if grpcserver :

			self.communicationservicer = communicationservicer
			communicate_pb2_grpc.add_CommunicateServicer_to_server ( self, grpcserver, )

		#	super ( Communicate, self, ).__init__ ( )	
		#	self.target			= self.say
		#	self.daemon 		= daemon
		#	self.name			= self.__class__.__name__
		
		#self.pipeline		= queue.Queue ( maxsize= int ( valet.ini.pool['valet']['main']['concurrency_slots'] ), )
		self.name 			= valet.ini.pool['valet']['attributes']['name']

		###################################################################
		#
		## 	Setup the speech engine to lookup phrases and speech partials
		#	to return during speech / writing through the communicate
		#	property
		#
		###################################################################
		#self.speak	= Speak ( valet, )
		
		###################################################################
		#
		## 	Setup the console properties for the cli and written i/o
		#
		###################################################################
		rows, columns		= subprocess.check_output ( ['stty', 'size'] ).split ( )
		
		self.console		= textwrap.TextWrapper (	initial_indent		= '%s> @%s ⇾' % ( self.colors.OKBLUE, self.name ), 
														width				= int ( columns ),
														replace_whitespace	= False,
													)
	
		return True









# 	def say ( self, ) :
# 		"""#######################################################################
# 	
# 		Say provides an additional wrapper to invoke both cli write &
# 		vocalized speech with .vocalize - only if vocalization is enabled
# 		within the config file main.  Processes list of strings to output
# 		or single string (which gets put into a list)
# 	
# 	    #######################################################################
# 		"""
# 		
# 		while True :
# 		
# 			try :
# 
# 				# Extract the next item from the communication pipeline
# 				corpus = self.pipeline.get ( timeout=1, )
# 				
# 				if corpus :
# 				
# 					self.valet.log.debug ( 'Communicate Corpus Received : %s' % corpus, )
# 					
# 					self.__saymapper ( corpus, )
# 					corpus.task_done ( )
# 					
# 				
# 			except queue.Empty :
# 				
# 				continue
# 						
# 
# 
# 	def _saymapper ( self, corpus, ) -> bool :
# 		"""#######################################################################
# 	
# 		Iterate over items in communication pipeline item if iterable, and process
# 		each item as a standalone communication event
# 	
# 		@output / str > string value to print as output from Valet
# 		
# 		Returns / bool > signifying completion
# 		
# 	    #######################################################################
# 		"""
# 
# 		if isinstance ( corpus, Iterable ) and not isinstance ( corpus, str ) :
# 		
# 			for _corpus in corpus :
# 			
# 				self.__saymapper ( _corpus, )
# 				
# 		else :
# 
# 			###################################################################
# 			#
# 			## 	Write to the stdout window unless otherwise expressed
# 			#
# 			###################################################################
# 			self._write ( corpus, )
# 	
# 			###################################################################
# 			#
# 			## 	Only send to speech module to vocalize the corpus if the speak
# 			#	service/functionality is enabled
# 			#
# 			###################################################################
# 			if self.speak.enabled :	
# 		
# 				self.speak.vocalize ( corpus, )
# 		
# 		
# 		return True
