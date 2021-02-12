###########################################################################
#
## @file callback.py
#
###########################################################################

# import os

###########################################################################

class Callback :
	"""###########################################################################
	
  	A wrapper for Valet to issue callback commands to itself chained with
	abilities.  This base class allows for quick instantiation of a callback
	object within the server/ability instantiation so as to operate in a 
	similar model to the base Ability class.

	TO DO
	
	###########################################################################
	"""	
	
	def __init__ ( self, callback, ) :
		"""#######################################################################
	    
    	Initialize with callback method definition to be internally assigned
    	for later - intentional servelet.execute( ) call within Server
    
    	@callback / method definition of the callback defined within ability
    
	    #######################################################################
	    """
		self.callback 	= callback
		
		
	def execute ( self, ) :
		"""#######################################################################
	    
    	Instance executor so the execution must be directly and intentionally
    	called rather than calling upon instantiation	
    
		#######################################################################
		"""
		
		return self.callback ( )
		
		
