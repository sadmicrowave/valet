###########################################################################
#
## @file wikipedia.py
#
###########################################################################

import re

import wikipedia
  
###########################################################################
#
##   A wrapper for Valet to call and interact with the wikipedia module.
#	 Providing and interface for Valet to make encyclopedia type lookups
#
###########################################################################


class Wiki :
	
	#######################################################################
    #
    ##	Load the wikipidia config information like api / keys, etc.
    #
    #	@db		/ object > db object pointer for querying against routes
    #	@ini	/ object > ini configs object
    #	@input	/ str > the raw input string from the user
	#
    #######################################################################
	def __init__ ( self, db, ini, input ) :
		
		self.db 	= db
		self.ini	= ini
		self.input	= input


	#######################################################################
    #
    ##	Instance executor so the execution must be directly and intentionally
    #	called rather than calling upon instantiation	
    #
    #######################################################################
	def execute ( self, ) :
		
		self.result = wikipedia.summary( self.input, sentences=3 ) or None
		
		print ( self )
		
		return self
	
	
	#######################################################################
    #
    ##	Override the class method to print the class
    #
    #######################################################################
	def __str__ ( self, ) :
		
		return "According to Wikipedia: " + re.sub("\n|\r|\t+|\s+", " ", self.result.capitalize()) if self.result else ''
		
		
		