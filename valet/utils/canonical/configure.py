###########################################################################
#
## @file configure.py
#
###########################################################################

import os, ntpath, glob

from configparser import ConfigParser

###########################################################################

class Configure:
	"""#######################################################################
	A wrapper for Valet to load config files 
	into assigned variables.  This can receive any project sub-directory and 
	file type suffix to scan, or receive a direct filename/path to load.
	#######################################################################
	"""
	#######################################################################
    #
    ##	Class level variables
    #
    #######################################################################
    pool 		= {}
    
    
	def __init__ ( self, dir=None, ext=None, filepath=None ) :
		"""#######################################################################
    
    	The constructor of the class, initialize with filepath read if exists,
    	then read from director if present
    	
    	@dir 	/ base directory to import files
    	@ext	/ extention of file types to iterate, iterates all if none
    	@filepath	/ direct filepath to import
	    
	    #######################################################################
	    """
	    		
		if filepath :
			self.__read ( filepath )
		
		if dir :
			self.__load_dir ( dir, ext )


	
	def __read ( self, filepath=None ) :
		"""#######################################################################
	    
	    Read the contents of the file into the instance and assign as dictionary 
	    
	    @filepath		/ string - filepath to locate config file
	    
			
	    #######################################################################
	    """
				
		if filepath and os.path.isfile( filepath ) :
			
			self.conf = ConfigParser( )
			self.conf.read( filepath, encoding='utf-8' )
			
			# Add the config contents to the config container, accessible
			# in the list by filename (minus extension)
			file = ntpath.basename( filepath ).split( '.ini' )[0]
			self.pool[ file ] = self.conf._sections
	
	
			
	def __load_dir ( self, dir=None, ext=None ) :
		"""#######################################################################
	    
    	Generate a temporary filename for each speech command that comes
     	in so the name of the file doesn't conflict or override each time.
    	Generate a hash string of the input text
    
		@dir 		/ string - directory to locate config files in
		@ext		/ string - file extension to filter search for onfig files
	    #######################################################################
		"""
		
		if dir and os.path.isdir ( dir ) :
			
			for filename in glob.glob( '%s/*%s' % ( dir, ext) ) :			
				self.__read ( filename )


