###########################################################################
#
## @file environment.py
#
###########################################################################

import os, logging

from logging.config import dictConfig

###########################################################################

class Environment :
	
	"""#######################################################################
	
	The Environment class defines and creates the directory structures necessary 
	for the output files from this program including actual file delivery 
	directory, archive dir, any temp dirs needed for file moves, and log 
	directory and file creation.  The class is also responsible for 
	instantiating the log handler/rotator for log outputs
	
	#######################################################################
	"""
	#######################################################################
    #
    ##	Class level variables
    #
    #######################################################################
	__log 		= None
	
	
	
	def __init__ (self, valet=None, ) :
		"""#######################################################################
	    
    	Initialize the class accepting valet as the main object
    
    	@valet	/ instance of valet itself to interact with main object
    
	    #######################################################################
	    """	
		self.valet		= valet	
		
	

	
	def setuplog ( self, ) :
		"""#######################################################################
	    
	    Initialize the log object and configure appropriately using configuration
	    values set in loaded .conf/*.ini files and passed within valet.  Setup the 
	    logging handler to create log entries from logger statements throughout 
	    valet and provides a rotator handler to prevent file sizes from increasing 
	    too large.  Create the logger config dictionary, this is a simple JSON array 
	    which is loaded into the log module and used to configure the python logger 
		with the option we want.
    	
	    #######################################################################
		"""
		LOG_SETTINGS = {	 
				 'version' : 1
				,'handlers': {
								'core': {
									 # make the logger a rotating file handler so the file automatically gets archived and a new one gets created, preventing files
									 # from becoming too large they are unmaintainable. 
									 'class'		: 'logging.handlers.RotatingFileHandler'
									 # by setting our logger to the DEBUG level (lowest level) we will include all other levels by default
									,'level'		: self.valet.ini.pool['valet']['log']['level']
									 # this references the 'core' handler located in the 'formatters' dict element below
									,'formatter'	: 'core'
									 # the path and file name of the output log file
									,'filename' 	: os.path.join( self.valet.ini.pool['valet']['log']['locale'], '%s.log' % self.valet.name )
									,'mode'			: 'a'
									 # the max size we want to log file to reach before it gets archived and a new file gets created
									,'maxBytes'		: int ( self.valet.ini.pool['valet']['log']['size'] )
									 # the max number of files we want to keep in archive
									,'backupCount' 	: int ( self.valet.ini.pool['valet']['log']['backups'] )
								}
				}
				 # create the formatters which are referenced in the handlers section above
				,'formatters': {
								'core': {
									'format': '%(levelname)s %(asctime)s %(module)s|%(funcName)s %(lineno)d: %(message)s' 
									#"[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
								}
				}
				,'loggers'	 : {
								'valet': {
									 'level' 	: self.valet.ini.pool['valet']['log']['level']
									,'handlers'	: ['core']
								}
				}
			}
	
		###################################################################
		#
		#	Use the built-in logger dict configuration tool to 
		#	convert the dict to a logger config
		#
		###################################################################
		dictConfig ( LOG_SETTINGS )

		###################################################################			
		#
		#	Get the logger created in the config and named root 
		#	in the 'loggers' section of the config
		#
		###################################################################
		self.__log = logging.getLogger ( 'valet' )
					
		
		return self.__log
		
	###################################################################
	#
	## 	Set class / instance properties with setters
	#
	###################################################################
	@property
	def log ( self, ) :
		
		return self.__log
		
		
		
		