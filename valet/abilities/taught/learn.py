###########################################################################
#
## @file learn.py
#
###########################################################################

import os, sys, re, requests

from urllib.parse import urlparse

from ..ability import Ability
  
###########################################################################
#
##   A wrapper for Valet to add a website or file to the learning database
#	 and repository for valet's intelligence to increase / grow.
#
###########################################################################


class Learn ( Ability ) :
	
	#######################################################################
    #
    ##	Class level variables
    #
    #######################################################################
	content		= None

	#######################################################################
    #
    ##	Instantiation of learn ability, should take text from varying
    #	sources and perform text copies to the intelligence directory
    #	for future learning initiatives
    #
    #	@valet	/ instance of valet itself to interact with main object
    #	@input	/ str > the raw input string from the user
    #
    #######################################################################
	def __init__ ( self, valet, input=None, ) :
		
		self.valet		 = valet
		
		self.intel_store = valet.ini.pool['intelligence']['structure']['locale']
		self.input		 = self.__cleanse ( input, )		
		
		
	#######################################################################
    #
    ##	Instance executor so the execution must be directly and intentionally
    #	called rather than calling upon instantiation.  Here, we split
    #	out operations depending on what the learning resource type is.	
    #
	#	Returns: indicator string for successfully learned / error
	#
    #######################################################################
	def execute ( self, ) :
		
		try :	
			if self.__is_url ( self.input, ) :
			
				content = self.__gather_site_text ( self.input, )
				if self.__write_to_file ( self.input, content ) :
					
					return "Successfully added %s to the learning repository." % self.input
			
		except requests.ConnectionError as e :		
			# input/url does not exist on the internet
			raise e

	
	
	#######################################################################
    #
    ##	Cleanse the input string of initial user input words and other
    #	nondesireable content before attempting to learn provided resources.
    #	Assumes last structure in provided sentence for this ability is
	#	the path.
    #
    #	@input	/ str > raw input string from user
    #	Returns: formatted & cleansed str
    #
    #######################################################################
	def __cleanse ( self, input, ) :
		
		# split the string and return the last element to check against is_url
		return input.split ( ' ' ) [ -1 ]
		
	
	
	#######################################################################
    #
    ##	Determine if the input string to learn is a url to attempt to gather
    #	the text from the url source
    #	Example: http://www.example.com = True
    #			 example.com			= False
    #
    #	@input	/ str > the raw input string from the user
    #	Returns : list of urlparsed site url data or False
	#
    #######################################################################
	def __is_url ( self, input, ) :

		try :
		    result = urlparse ( input )
	
		    return all ( [ result.scheme, result.netloc ] )
		
		except ValueError :
		
		    return False
	
	
	
	#######################################################################
    #
	##	Attempt to gather the site context / text 
	#
    #	@input	/ str > the raw input string from the user
    #	Returns : str buffer to write to file object
	#
    #######################################################################
	def __gather_site_text ( self, input, ) :
				
		return requests.get ( input ).text
	
	
	
	#######################################################################
    #
	##	Write the content to a file for learning in the language learning
	#	process
	#
    #	@url		/ str > input string url component
    #	@content	/ str > buffer string from input source to write
    #	Returns : str buffer to write to file object
	#
    #######################################################################
	def __write_to_file ( self, url, content, ) :
		
		###################################################################
		#
		##	Construct the unique filename to create and store contents
		#
		###################################################################
		#now			= datetime.datetime.now( ).strftime( "%Y%m%d-%H%M%S" )
		urlbase		= url.split("//")[-1].split("/")[0].split('?')[0]
		path		= os.path.join ( self.intel_store, 'unlearned', urlbase )
		
		with open ( path, "wb" ) as f :
			f.write ( content.lower( ) )
			
		return True
		
		