###########################################################################
#
## @file exit.py
#
###########################################################################

import os

from ..ability import Ability
  
###########################################################################
#
##   A wrapper for Valet to exit itself
#
###########################################################################

class Exit ( Ability ):

	#######################################################################
    #
    ##	Exit construct callback for exiting system
    #
    #	@valet	/ instance of valet itself to interact with main object
    #	@input	/ str > the raw input string from the user
    #
    #######################################################################
	def __init__ ( self, valet, input=None ) :
			
		self.valet 	= valet
					

	#######################################################################
    #
    ##	Instance executor so the execution must be directly and intentionally
    #	called rather than calling upon instantiation
    #
    #######################################################################
	def execute ( self, ) :
		
		return "Goodbye, sir."
		
	
	###################################################################
	#
	## 	Implement callback from the base Ability class
	#	
	#	@future > object holding future execution details from thread
	#			pool manager
	#
	###################################################################
	def callback ( self, future=None, ) :
		
		self.valet.intelligence.save ( )
		
		raise SystemExit ( )	