###########################################################################
#
## @file stopwatch.py
#
###########################################################################

import time

from functools import wraps


###########################################################################
#
##   Stopwatch provides a wrapper for timing interactions and execution
#	 times, and times between certain measured events
#
###########################################################################
class Stopwatch :
	
	#######################################################################
    #
    ##	Class level variables
    #
    #######################################################################
	
		
	#######################################################################
    #
    ##	Initialize the class
    #
	#######################################################################
	def __init__ ( self, ) :
	
		pass
		
	
	#######################################################################
    #
    ##	Add data to the Fifo object
    #	
    #	@data > str|bool|list|dict|None|int|any. / any item to be appended
    #			/ to the fifo object
    #
	#######################################################################
	def methodtimer ( method, ) :

		@wraps ( method )
		def wrapper ( *args, **kwargs ) :
			
			start_time	= time.time ( )
			result		= method ( *args, **kwargs )
			end_time	= time.time ( )
		
			print( f"{method.__name__} => {(end_time-start_time)*1000} ms" )
			return result
		
		return wrapper	
		
	
  