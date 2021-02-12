###########################################################################
#
## @file task.py
#
###########################################################################

import os, datetime

from threading import Thread
from threading import Event

###########################################################################

class Task ( Thread ) :
	"""###########################################################################
	
	A class for Valet's server to instantiate a task to thread / process.
	This object is passed back and managed within Valet's server or
	pre-frontal cortex
	
	###########################################################################
	"""	
	#######################################################################
    #
    ##	Class level variables
    #
    #######################################################################
	name 		= None
	duration	= None
	action		= None
	future 		= None
	
	
	def __init__ ( self, action, ) :
		"""#######################################################################
	    
    	Initialize the class to build the task instance usable within the server
    	functions to standardize input tasks
    
    	@action > str / action to assign and execute within the threaded task
    
		#######################################################################
		"""
		self.action 		= action
		self.__starttime 	= datetime.datetime.now ( )
		self.exit_event		= Event ( )
	
		Thread.__init__ ( self )
		
				

	def status ( self, ) :
		"""#######################################################################
	    
    	Provides report out of current status of Thread 
    	including execution status and execution time (duration), name, etc.
    
		#######################################################################
		"""		
		
		return """
		Name: %s
		State: %s
		Duration: %s
		""" % (	self.name, 
				'Completed' if not self.is_alive ( ) else 'Working', 
				self.duration 
			)
		
				
	
	def __str__ ( self, ) :
		"""#######################################################################
	    
	   	Override str of class to print results of self execution
	   
		#######################################################################
		"""				
		return self.future.result ( ) if self.future.result ( ) else ''
		
	
	
	
	@property 
	def duration ( self, ) :
		"""#######################################################################
	    
    	Duration is a property that calculates the current time duration
    	of the task running
    	
    	Returns: str > time delta of execution start to now
    
		#######################################################################
		"""
		return str ( datetime.timedelta ( seconds = abs ( self.__starttime - datetime.datetime.now ( ) ) ) )
		
		
	
	###################################################################
	#
	## 	Set class / instance properties with setters
	#
	###################################################################	
	@property
	def exit ( self, ) :
		return self.__exit
		
	@exit.setter 
	def exit ( self, val ) :
		
		if self.event :
			self.exit_event.set ( )
		
		self.join ( )
		return self.status ( )
		


	#######################################################################
    #
    ##	Execute allows explicit controlled execution of the task and the
    #	tasks action object
    #
	#######################################################################
	#@property 
	#def execute ( self, ) :
	#	
	#	return self.action.execute


	