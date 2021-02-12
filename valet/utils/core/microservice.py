###########################################################################
#
## @file process.py
#
###########################################################################

import threading

#from multiprocessing import Process, Queue, get_context

###########################################################################


class Microservice ( threading.Thread ) :
	"""###########################################################################
	A wrapper for Valet to split tasks into separate processes using
	a ProcessPoolManager and allowing each to communicate using central
	global session - this class is designed to be an abstract base class
	used to make objects extending this class able to split into a separate
	process and access the main memory location of valet for data sharing

	###########################################################################
	"""

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
	def __init__ ( self, pipeline, event, func, daemon=True, 
					group=None, target=None, name=None, 
					args=(), kwargs=None, verbose=None, ) :
		
		super ( Microservice, self, ).__init__ ( )
		self.pipeline 	= pipeline
		self.event		= event 
		self.daemon 	= daemon
		self.target 	= func
		self.name		= func.__class__.__name__
		
	
	
	def run ( self, ) :
		"""#######################################################################
    
    	Handles what to run when the thread / daemon is started
    
	    ########################################################################
		"""
	
		self.target ( )
	
	
		
	#######################################################################
    #
    ##	Explicitly initalizes the process as a new forked process, starts
    #	the process and returns the process object to be stored in the
    #	original call.  By default processes are daemonized.
    #
	#	Returns: process object
    #
    #######################################################################	
	# 	def fork ( self, func, daemonize, ) :
	# 		
	# 		#def localrun ( ) :
	# 		#	print ('localrun')
	# 		#	#listener.run ( )
	# 			
	# 		
	# 		process = Process ( target=func,
	# 							daemon=daemonize, 
	# 							name=func.__class__.__name__,
	# 						)
	# 						
	# 		process.start ( )
	# 	
	# 		return process
	
	
		
	#######################################################################
    #
    ##	Set notimplementederror for run to ensure any extending class
    #	implements this method.  The run method for each class extending
    #	multiprocessor should be an indefinite loop with an input and output
    #	buffer accessible to itself and main process
    #
    #######################################################################	
	#def run ( self, ) :
	#	
	#	raise NotImplementedError
			