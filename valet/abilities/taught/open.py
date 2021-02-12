###########################################################################
#
## @file open.py
#
###########################################################################

import os, mmap, tarfile
import concurrent.futures

#from pyunpack import Archive
#from ..ability import Ability
  
###########################################################################
#
##   A wrapper for Valet to open various types of files, objects, zips
#	 folders, etc. and return the contents
#
###########################################################################


class Open :
	
	#######################################################################
    #
    ##	Class level variables
    #
    #######################################################################
	corpus		= None

	#######################################################################
    #
    ##	Instantiation of ability - main setup 
    #
    #	@valet	/ instance of valet itself to interact with main object
    #	@input	/ str > the raw input string from the user
    #
    #######################################################################
	def __init__ ( self, valet, input=None, ) :

		self.input 		 = input
		_ 				 = self.__configure ( )


	#######################################################################
    #
    ##	Instance executor so the execution must be directly and intentionally
    #	called rather than calling upon instantiation.  Here, we split
    #	out operations depending on what the learning resource type is.	
    #
	#	Returns: indicator string for successfully learned / error
	#
    #######################################################################
	def execute ( self, corpus=None ) :
		
	 	###################################################################
	 	## Opener for files
		if os.path.is_file ( self.input, ) :
			
			corpus = self.__unpack ( self.input )
				
		
		###################################################################
		#	Theroretically, we could build more types of openers here,
		# 	for things other than files.
		
		
		return corpus
	
	
	
	#######################################################################
    #
    ##	Unpack is used to evaluate the input filename and determine the most
    #	appropriate method for unpackacking / opening the contents to a 
    #	returnable object - define handlers as the internal method list
    #	of corresponding unpacking methods based on file extention.
    #
    #	@f 	/ str > filename to parse
    #	Returns : file contents object
    #
    #######################################################################
	def __unpack ( self, f, ) :

		# 	Get the pattern from the filename extension
		pattern = os.path.splitext ( f ) [1] [1:]
							
		###################################################################
		#
		##	Attempt the lookup of the extension within the defined handlers
		#	if it idesn't exist handle the exception gracefully
		#
		###################################################################
		try :
				
			return self.handlers [ pattern ] ( f )
		
		except KeyError as e :
		
			Exception ( 'No unpacking pattern found for `%s` file types' % pattern )
	
			
	
	
	#######################################################################
    #
    ##	Unpack_tar is used to extract and unpack contents of a tar.gz
    #	compressed file
    #
    #	@filename 	/ str > filename to open and parse
    #	@permissions / str > opening permissions (r|w|e)
    #	compressiontype / str > ending compression (e.g.: 'gz')
    #	Returns : text from unpacked file or file set
    #
    #######################################################################
	def __unpack_tar ( self, filename, permissions='r', compressiontype=None, _corpus='', ) :

		if tarfile.is_tarfile ( filename ) :
		
			extension 			= filename.split ( '.' )[-1:]
			allowed_compression = ['gz']
			compressiontype 	= ':%s' % extension if extension in allowed_compression else compressiontype	
			tar 				= tarfile.open ( filename, '%s%s' % ( permission, compressiontype ) )
			members 			= tar.getmembers ( )
			
			for member in members :
				
				if member.isfile ( ) and not member.issym ( ) :

					file	= tar.extractfile ( member )
				
					_corpus.append ( self.__unpack ( file ) )
					
			tar.close ( )
		
		return _corpus
	
	
	
	#######################################################################
    #
    ##	Open the file with options passed as permissions (r/w/e) and 
    #	binary opener operatory.  mmap bypasses the usual I/O buffering 
    #	by loading the contents of a file into pages of memory.
    #
    #	@filename 	/ str > filename to open and parse
    #	@permissions / str > opening permissions (r|w|e)
    #	@binary / bool > whether to open as binary or not
    #	Returns : text from the opened source file
    #
    #######################################################################
	def __open ( self, filename, permissions='r', binary=True, _corpus=None, ) :
		
		with open ( filename, '%s%s' % ( permissions, 'b' if binary else '' ) ) as file :
			 
			_corpus = mmap.mmap ( file.fileno ( ), 0 )

		return _corpus
		
	
	
	#######################################################################
    #
    ##	Perform any setup needed for the  class  to do it's job.  
    #
    #	@valet	/ instance of valet itself to interact with main object
	#
    #######################################################################
	def __configure ( self, valet, ) :

		self.valet		= valet
		self.workers	= int ( valet.ini.pool['valet']['main']['workers'] )		

		self.handlers 	= { 'csv' 	: self.__unpack_csv,
							'tar'	: self.__unpack_tar,
							'gz'	: self.__unpack_tar,
							'html'	: self.__unpack_html,
							'txt'	: self.__unpack_txt,
							'json'	: self.__unpack_json,
						}
		
		return

