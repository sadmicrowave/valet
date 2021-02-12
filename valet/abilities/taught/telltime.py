###########################################################################
#
## @file telltime.py
#
###########################################################################

import datetime
  
###########################################################################
  
class Telltime :
	"""#######################################################################
	A wrapper for Valet to call and interact with the datetime module.	
	Returning the current time
	
	Params
	@valet	/ instance of valet itself to interact with main object
	@input	/ str > the raw input string from the user
	
	Returns / str > current time stamp
	#######################################################################
	"""
	
	def __init__ ( self, valet=None, input=None, ) :
		
		pass
		#self.valet	= valet


	#######################################################################
    #
    ##	Instance executor so the execution must be directly and intentionally
    #	called rather than calling upon instantiation	
    #
	#	returns printed string of current time
	#
    #######################################################################
	def execute ( self, ) -> str :
			
		return "The time is %s" % datetime.datetime.now( ).strftime ( "%H:%M:%S" )