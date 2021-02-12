###########################################################################
#
## @file server.py
#
###########################################################################

import os, queue, threading, traceback
import concurrent.futures 

from concurrent.futures import ThreadPoolExecutor

from .task import Task

###########################################################################

class Server : 
	"""###########################################################################
	
	A wrapper for Valet to issue commands to itself.  Essentially this
	is Valet's core worker factory where threads are created, managed,
	stored, interacted-with, and retrieved from.
	
	TO DO
	1. BUG - On abilities with callback, callback seems to be executed before .execute
		is printed/returned
	
	###########################################################################
	"""
	#######################################################################
    #
    ##	Class level variables
    #
    #######################################################################
	listen				= True
	executor			= None

	
	def __init__ ( self, valet=None, ) :
		"""#######################################################################
	    
    	Initialize thread manager / server to handle and interact with
    	calls within Valet.  Ultimately this should run as a daemon monitor
    	with helper functions to aide in rogue operation cleanup, timing and
    	performance monitoring, etc.
    
    	@valet	/ instance of valet itself to interact with main object
	    
	    #######################################################################
		"""	
		
		_		= self.__configure ( valet, )
				
				
	
	def run ( self, ) :
		"""#######################################################################
	    
		Run is required for all classes extending from base class Process.
		This method handles the main run loop of the daemon process, which
		should be wait for input on the input buffer queue.  Later, we can
		expand this to look for some signals to interact with more
		robust commands.
	
		Run has access to all attributes and helper definitions defined
		in the class implementing Process, so nothing additional needs to be
		passed, unless explicitly desired to not place it on self instance
		of the implementer.
		
	    #######################################################################
		"""
		
		while True :
			
			try :
			
				task = self.pipeline.get ( timeout=1, )
				
				if task :
				
					self.valet.log.debug ( 'Server Task Received : %s' % task, )
					self.serve ( self.standardize ( task, ) )
				
			except queue.Empty :
				
				continue
				
				
		
	def serve ( self, task, executor=None, futures={}, ) -> bool :
		"""#######################################################################
	    
		Serve is a method wrapper used for the Server manager to execute
		a list of dictionaries of each execution type that should be done 
		in a pool.
	
		@tasks 		/ list > list of object items to instantiate and serve
		@executor 	/ obj > provides explicit threading executor pool, or uses 
						\ default from self.__configure
		Returns 	/ bool > signifying completion
	
		TO DO
		1. Add ProcessPoolExecutor for outside python commands - os commands
		2. Add split-outs for different types of objects within servelet_pool
	
	    #######################################################################
		"""
		
		with executor or self.__default_executor as self.executor :
			
			self.executor.map ( self.__taskmapper, task, )
			
			###############################################################
			#
			## 	Set the completion activity when the thread finishes, if 
			#	result is present on future.result(), or returning the 
			#	entire future object provides result back to caller
			#	self._futuresbuffer [ future ] = task return from .map ^
			#
		    ###############################################################
			for future in concurrent.futures.as_completed ( self._futuresbuffer, ) :

				task.task_done ( )
			
				self.valet.communicate.pipeline.put_nowait ( self._futuresbuffer [ future ], )
		
		return True	
			
				
	
	def standardize ( self, task, ) -> list :
		"""#######################################################################
	
		Standardize given input into Task objects for the server to process
		and interact with in a standardized fashion
	
		@input  / list > list of action, items to execute in a thread task
		Returns / list > list of Task objects (one for each input action)
		
		#######################################################################
		"""	
		
		return [ Task ( action, ) for action in task if not isinstance ( action, Task ) ]
		
	
	
	def __taskmapper ( self, task, ) -> bool :
		"""#######################################################################
	   
		Standardize given input into Task objects for the server to process
		and interact with in a standardized fashion
		
		@input 	/ list > list of action, items to execute in a thread task
		Returns / bool > signifying completion
		
	    #######################################################################
		"""
		
		try :

			task.future = self.executor.submit ( task.action.execute, )
							
			###################################################################
			#
			## 	Set the completion activity when the thread finishes - 
			#	this is the threaded ability callback				
			#
		    ###################################################################
			if hasattr ( task.action, 'callback', ) : 
				
				task.future.add_done_callback ( task.action.callback, )
		
			#	Add task to futuresbuffer dict for matching as_complete
			self._futuresbuffer [ task.future ] = task

		except Exception as e :
			
			self.valet.log.error( "ERROR - %s" % traceback.format_exc ( ) )
		
		
		return True

	

	
	def __configure ( self, valet, ) -> bool :
		"""#######################################################################
    
    	Perform any setup needed for the  class  to do its job.
    
    	@valet	/ instance of valet itself to interact with main object
		Returns / bool > signifying completion
	
		#######################################################################
		"""
		
		self.valet 					= valet
	
	#	super ( Server, self, ).__init__ ( )
	#	self.target					= self.run
	#	self.daemon 				= daemon
	#	self.name					= self.__class__.__name__

		#self.__default_executor 	= ThreadPoolExecutor ( max_workers = int ( valet.ini.pool['valet']['main']['workers'] ) or None, 
														)
		
		self._futuresbuffer			= {}
		#self.pipeline				= queue.Queue ( maxsize= int ( valet.ini.pool['valet']['main']['concurrency_slots'] ), )
		
		
		return True

