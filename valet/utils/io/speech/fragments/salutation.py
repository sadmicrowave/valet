###########################################################################
#
## @file salutation.py
#
###########################################################################

# import datetime

###########################################################################
#
##   A wrapper for Valet to provide a greeting when speaking
#
#    This will be the prefix statement in sentences / responses.
#
###########################################################################

class Salutation:
	
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
		# Build this section out later after voice / input gender
		# identification is included ( sir / maam )

		input_voice = 'M' # Male
		
		if input_voice == 'M' :
			
			return "sir"
		
		elif input_voice == 'F' :
			
			return "ma'am"
	   
	   
	