###########################################################################
#
## @file greeting.py
#
###########################################################################

import datetime

###########################################################################
#
##   A wrapper for Valet to provide a greeting when speaking
#
#    This will be the prefix statement in sentences / responses.
#
###########################################################################

class Greeting:
	
	DIR = '/data/speech/'
	
	#######################################################################
	#
	##	The constructor of the class
	#
	#######################################################################
	def __init__( self, ) :
		
		pass
		
	
	
	#######################################################################
	#
	##	What to return if the caller prints this class
	#
	#######################################################################
	def __str__ ( self, ) :

		hour = int( datetime.datetime.now().hour )
		
		if hour >= 0 and hour < 12 :
			return "Good morning"
		elif hour >= 12 and hour < 18 :
			return "Good afternoon"
		else: 
			return "Good evening"
	   
	   
	