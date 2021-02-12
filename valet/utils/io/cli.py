###########################################################################
#
## @file cli.py
#
###########################################################################

import os, io, sys, traceback
 
from cmd import Cmd

###########################################################################

class CommandLineInterface ( Cmd ):
	
	"""###########################################################################
	
	A wrapper for Valet to read and write to a Command Line Interface /
	Interactive Interpreter / Prompt
	
	Valet must be able to accept input from various sources and determine
	which is the most applicable to use - cli will be a backbone interface
	required for all input and output as data will be passed from device
	to-and-from cli
	
	###########################################################################
	"""
	#######################################################################
	#
	## 	Set class level variables based on CLI configuration
	#
	#######################################################################
	prompt		=	None
	completekey	=	'tab'
	intro		= 	None
	banner		=	"""
====================================================================
####################################################################

888888b.                                          
888  "88b                                         
888  .88P                                         
8888888K.  .d88b. 88888b. .d8888b  .d88b. 88888b. 
888  "Y88bd8P  Y8b888 "88b88K     d88""88b888 "88b
888    88888888888888  888"Y8888b.888  888888  888
888   d88PY8b.    888  888     X88Y88..88P888  888
8888888P"  "Y8888 888  888 88888P' "Y88P" 888  888

Copyright (C)  Sadmicrowave

Documented commands ( type help <topic> )

####################################################################
====================================================================
"""

	
	def instantiate ( self, valet=None, ) -> bool :
		"""#######################################################################
		
		The mock-constructor of the class since the Cmd module doesn't allow to 
		override __init__, or at least this seems better practice
	
		@valet	/ instance of valet itself to interact with main object
	
		#######################################################################
		"""
			
		self.valet 	= valet
		self.prompt	= '%s> @%s  ⇾ ' % ( valet.colors.WARNING, 'Guest' )
		
		print ( '%s\n' % self.banner )
		
		return True

		
	
	
	def cmdloop ( self, intro=None, ) :
		"""#######################################################################
		
		Override the default cmdloop in order to add a Keyboard
		Interrupt handler
		
		#######################################################################	
		"""
		
		self.do_clear ( )
				
		while True : 
		
			try :
			
				super ( CommandLineInterface, self ).cmdloop ( intro='' )
				break
				
			###############################################################
			#
			## 	Gracefully handle Ctrl+C terminal interrupt - requiring 
			#	user to exit with predefined exit() command
			#
			###############################################################
			#except KeyboardInterrupt :
			#
			#	print("^C")
				
			except Exception as e :
			
				self.valet.communicate.pipeline.put_nowait ( "I'm sorry %s, I seem to have encountered a problem:\n\n%s%s %s\n" 
											% (	self.valet.communicate.salutation, 
												self.valet.colors.FAIL, 
												traceback.format_exc(), 
												self.valet.colors.ENDC
												) 
											)

	def default ( self, input, ) :
		"""###################################################################
		
		Handle default expression if command is unknown, attempt command
		lookup in the appropriate db / table & bubble provided response,
		or, if no alternative route is found in db lookup, then provide
		generic response back to user.  Here Valet determines the response 
		type to provide.  Lookup from taught abilities within the valet 
		database, check against intelligence sources, then lookup from 
		wikipedia, then wolframalpha, then etc. etc. etc... all handled
		within the valet.intelligence.process method
	
		@input	/ str > the raw input string from the user
		
		###################################################################	
		"""

		self.valet.intelligence.process ( input, )
		
					
			
	
	def do_clear ( self, args=None, ) :
		"""###################################################################
		
	 	Provide the ability to clear the console, also execute this
		upon start-up
		
		@args		/ default args passed by cmdloop
	
		###################################################################
		"""	
		# for windows 
		if os.name == 'nt': 
		
			_ = os.system ('cls')
		
		# for mac and linux(here, os.name is 'posix') 
		elif os.name == 'posix' : 
		
			_ = os.system ('clear') 
	
			
			
	
	
	def do_EOF ( self, args=None, ) -> bool :
		"""###################################################################
		
	 	Handle the provided user input, including any interpretation,
		modulation, breakdown, matching, or other operations
		
		@args		/ default args passed by cmdloop
		@Returns	/ bool signifying completion
	
		###################################################################
		"""	
		return True	


		
	