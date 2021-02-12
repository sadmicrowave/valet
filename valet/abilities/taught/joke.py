###########################################################################
#
## @file joke.py
#
###########################################################################

import pyjokes

###########################################################################

class Joke :
	"""#######################################################################
	A wrapper for Valet to call and interact with the jokes module. Returning 
	a random joke from the provided joke sources and input mechanisms
	    
	Params
	@valet	/ instance of valet itself to interact with main object
	@input	/ str > the raw input string from the user
	
	Returns / str > new random joke string
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
    #######################################################################
	def execute ( self, ) -> str :
		
		return pyjokes.get_joke( ).capitalize( )