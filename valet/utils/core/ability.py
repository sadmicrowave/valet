###########################################################################
#
## @file ability.py
#
###########################################################################

import os, re, importlib

from .callback import Callback

###########################################################################

class Ability :
	"""###########################################################################
	
	A wrapper for Valet to lookup learned and taught abilities.  This
	includes looking up the ability in the associated database/table
	and executing that ability if found, if not, handle otherwise.  This is
	the instance factory for abilities - all extend from here
	
	TO DO
	
	###########################################################################
	"""
	#######################################################################
    #
    ##	Class level variables
    #
    #######################################################################
	found		= False
	abilities 	= None
	
	
	def __init__ ( self, valet=None, ) :
		"""#######################################################################
    
    	Initialize the class accepting input from command and db object
    	pointer for querying. 
    
    	@valet	/ instance of valet itself to interact with main object
	    
	    #######################################################################
	    """	
	    
		self.valet		= valet
		
	
	def search ( self, input, ) :
		"""#######################################################################

		Search the valet database for routes with corresponding words
		associated as tags from the 'tags' table.  The relationship returns
		the top matching route after counting all matching tags found in
		the input string
		
		@input	/ str > the raw input string from the user
		Returns: list of instantiated abilities
		
		TO DO
			
		#######################################################################
	    """
	    
		tags		= self.__cleanse ( input ).split( ' ' )
		assurance	= float( self.valet.ini.pool['valet']['personality'] ['assurance'] ) / 100
		query 		= """SELECT routes.*, tags.*, 
							COUNT(route_id) AS _cnt,
							ROUND( 1.0 * COUNT(route_id) / %s, 2 ) as _percent
						FROM routes
							JOIN tags USING ( route_id )
						WHERE tags.tag IN ( '%s' )
						GROUP BY route_id
						%s
						ORDER BY _percent DESC
						""" % ( len ( tags ), 
								self.__construct_tag_string ( tags ),
								( 'HAVING _percent >= %s' % assurance ) if assurance else ''
							)
		
		self.valet.database.query( query )
					
		###################################################################
		#
		##	Iterate over all tetchall records and convert the row into a 
		#	dictionary object and put into a list to pass to _locate to
		#	instantiate for use
		#
		###################################################################
		results			= self.valet.database.cursor.fetchall ( )
		
		if results :
			routes			= [ dict( row ) for row in results ]

			self.valet.log.debug ( 'db.query results: %s' % results )
			self.abilities	= self.__locate ( input, routes=routes ) or None
	
		return self.abilities


	
	def __locate ( self, input, routes=[], ) :
		"""#######################################################################
	    
    	Attempt to locate the ability package returned from the _search
    	query.  Ex: my_package.my_directory.my_module.MyClass
    
    	@input	/ str > the raw input string from the user
    	@routes / list of dicts returned from query > default is wolframalpha
    
    	Returns: list > list of located abilities
    
	    #######################################################################
	    """
		
		__abilities = []
		
		# routes = routes or [{'name':'.wolfram', 'path':'abilities.taught'}]
		
		###############################################################
		#
		##	Iterate over retrieved routes from db query of available 
		#	abilities.  Instantiate the found ability and add to buffer 
		#	list of abilities to execute within ThreadManager
		#
		###############################################################
		for route in routes :
			
			_package	= importlib.import_module ( route['name'], route['path'] )
			_class 		= route['name'][1:].title( )
			_ability	= getattr( _package, _class )
			__abilities.append ( _ability ( self.valet, input, ) )
						
		return __abilities
	
	
	
	#######################################################################
    #
    ##	Securely execute the found ability/ies, build this out later to execute
    #	within a docker or something more isolated than on this processor
    #	in case of execution failures or uncaught overflows, etc.
    #	Additionally, this method passes execution syntax to ThreadManager
    #	to create a thread for the process and manage accordingly.  This is
    #	handled here as _secure_execution is the last step within the Ability
    #	class, before handing off for the Ability.child to execute.
	#
    #	@abilities > list / instances of abilities in a list for executing
    #	Returns: FIFO List > container for thread future results
    #
    #######################################################################
	#def execute_found_abilities ( self, abilities, ) :
	#	
	#	return self.server.serve ( abilities, )


			
	def __cleanse ( self, input, ) :
		"""#######################################################################
    
    	Cleanse the input string of special characters to remove punctuation
    	allowing for better querying to ensure we are only querying words
    
    	@input	/ str > raw input string from user
    	Returns: formatted & cleansed str
    
	    #######################################################################
	    """
	
		return re.sub ('[^A-Za-z0-9 ]+', '', input )



	
	def __construct_tag_string ( self, tags, ) :
		"""#######################################################################
	    
    	Format the input string elements accordingly to be used within the
    	query.
    	Example: 'tell me a funny joke'
    
    	@tags	/ list of space separated raw input
    	Returns: str > "'tell','me','a','funny','joke'"
    
	    #######################################################################
	    """
		
		return ("','").join( tags )
		
		

	###################################################################
	#
	## 	Set class / instance properties with setters
	#
	###################################################################
	@property 
	def abilities ( self, ) :
		return self.__abilities
	
	@abilities.setter
	def abilities ( self, value, ) :
		self.__abilities = value
		
		# If abilities, set the self.found property to True
		self.found = True if value else False

	
