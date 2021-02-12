###########################################################################
#
## @file restart.py
#
###########################################################################

import os, sys, time, psutil

from ..ability import Ability
  
###########################################################################
#
##   A wrapper for Valet to restart itself
#
###########################################################################

class Restart ( Ability ):

	#######################################################################
    #
    ##	Exit construct callback for gracefully exiting and restarting valet
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
		
		return "Restarting, %s.  Just a moment..." % self.valet.communicate.salutation
		
	
	###################################################################
	#
	## 	Implement callback from the base Ability class
	#	
	#	@future > object holding future execution details from thread
	#			pool manager
	#
	###################################################################
	def callback ( self, future=None, ) :

		p = psutil.Process ( os.getpid ( ) )
		
		for handler in p.open_files ( ) + p.connections ( ) :
		
			os.close( handler.fd )
		
		# Relaunching script
		python = sys.executable
		os.execl ( python, python, *sys.argv, )
		
		
		
	