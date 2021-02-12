###########################################################################
#
## @file wolframalpha.py
#
###########################################################################

import re

import wolframalpha
  
###########################################################################
#
##   A wrapper for Valet to call and interact with the wolframalpha module.
#	 Providing and interface for Valet to make calculations and do other
#	 types of data lookups
#
###########################################################################


class Wolfram ( Ability ) :

	#######################################################################
    #
    ##	Load the wolframalpha config information like api / keys, etc.
    #
    #	@valet	/ instance of valet itself to interact with main object
    #	@input	/ str > the raw input string from the user
    #
    #######################################################################
	def __init__ ( self, valet, input=None ) :
		
		self.ini	= valet.ini
		self.input	= input


	#######################################################################
    #
    ##	Instance executor so the execution must be directly and intentionally
    #	called rather than calling upon instantiation	
    #
    #######################################################################
	def execute ( self, ) :
		
		client = wolframalpha.Client ( self.ini.pool['api']['wolframalpha']['app_id'] )
		
		response 	= client.query( self.input )
		# Wolfram cannot resolve the question
		if response['@success'] == 'false' :
			self.result = None
			
		# Wolfram was able to resolve question
		else :
		
			result = ''
			# pod[0] is the question
			pod0 = response['pod'][0]
			# pod[1] may contains the answer
			pod1 = response['pod'][1]
			# checking if pod1 has primary=true or title=result|definition
			if ( ('definition' in pod1['@title'].lower() ) or ('result' in  pod1['@title'].lower()) or (pod1.get('@primary','false') == 'true')):
				# extracting result from pod1
				result = self.resolveListOrDict( pod1['subpod'] )		
		
			self.result = result or None #= next(self.response.results, None).text
		
		print ( self )
		
		return self
		
		
	
	#######################################################################
    #
    ##	Extracting Item from Pod — Resolving List or Dictionary Issue.  
    #	If the pod has several subpods, then we select the first element 
    #	of the subpod and return the value of the key “plaintext”. Else, 
    #	we just return the value of the key “plaintext”
    #
    #######################################################################
	def resolveListOrDict (self, variable, ) :
		
		if isinstance ( variable, list ) :
		
			return variable [ 0 ] [ 'plaintext' ]
		
		else :
		
			return variable[ 'plaintext' ]



	#######################################################################
    #
    ##	Override the class method to print the class
    #
    #######################################################################
	def __str__ ( self, ) :
		
		return re.sub ( "\n|\r|\t+|\s+", " ", self.result.capitalize( ) ) if self.result else ''
		
		
		