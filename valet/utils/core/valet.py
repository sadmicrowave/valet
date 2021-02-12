###########################################################################
#
## @file valet.py
#
###########################################################################

import os 
import grpc

from . import communicate_pb2_grpc
from . import communicate_pb2

from .server import Server
from .environment import Environment
from .intelligence import Intelligence
from .communicate import Communicate
from .database import Database

from ..canonical.configure import Configure

from ..io.cli import CommandLineInterface

#from utils.canonical.microservice import Microservice

###########################################################################

class Valet ( dict, ) :
	"""#######################################################################
	
	Valet is the main class of this application - which initializes all core
	components of the bot, sets up the environment for running, and starts
	execution.
	
	#######################################################################
	"""
	#######################################################################
    #
    ##	Class level variables
    #
    #######################################################################
	preinitialized			= False
	initialized				= False
	commandlineinterface	= None

	
	def __init__ ( self, **kwargs, ) :
		"""#######################################################################
	    
    	Initialize Valet object with base components necessary to exist - later,
    	each of the Valet cortices are called and initiated within their own
    	initializer
    
    	@valet	/ instance of valet itself to interact with main object
	    
	    #######################################################################
		"""	
	
		_ 		= self.__configure ( **kwargs, )
	
	
	
	
	def initialize ( self, ) -> bool :
		"""###################################################################
		
		Initialize begins the boot process of Valet - this is separated from
		__init__ to control what items Valet needs to exist as an object
		(vars, log, config, etc.) and what Valet needs to exist as an AI. 
		A callable for Valet to initialize all its important components, modules,
		micro services, etc. in order to operate.  Here, the environment including
		logs, variables, containers, etc. will be initialized and managed
	 
		Returns / bool > signifying completion
		
		###################################################################
		"""
		
		self.log.info ( ".init [ starting... ] \\\\" )

		###################################################################
		#
		## 	Hippocampus | Make a connection to the necessary databases to 
		#	operate properly - and other model files for memory, here we
		#	need to open each memory file and attach to self for use in
		#	any additional processes
		#
		###################################################################
		self.database		= Database ( self, self.dbpath, )
		
		
		###################################################################
		#
		## 	BrocosArea is responsible for handling transforming thoughts,
		#	concepts into output text.  Setup the object wrapper for the 
		#	user to communicate with valet and vice-versa
		#
		###################################################################
		self.communicate	= Communicate ( self, )
		#self.communicate.start ( )
		self.log.info ( ".init [ communicate _ brocasarea ]" )


		###################################################################
		#
		## 	PreFrontalCortex | Initiatilize the Server Manager / Thread Manager 
		#	that valet will utilize to manage related threads.  Essentially this
		#	is Valet's core worker factory where threads are created, managed,
		#	stored, interacted-with, and retrieved from
		#
		###################################################################
		#self.server			= Server ( self, )
		##self.server.start ( )
		#self.log.info ( ".init [ server _ prefrontalcortex ]" )
	
		
		###################################################################
		#
		## 	Instantiate the main intelligence object which does the core
		#	analysis between input text, learned and existing abilities,
		#	and lookup sequences for generating responses to user prompts.
		#
		#	After instantiation, initiate a learning sweep of any source
		#	file within the intelligence directory not yet learned
		#
		###################################################################		
		#self.intelligence	= Intelligence ( self, )
		##self.intelligence.train ( )
		#self.log.info ( ".init [ intelligence _ ]" )
		



		###################################################################
		#
		## 	Start the grpc services instantiated and registered with the 
		#	grpc server above
		#
		###################################################################
		self.grpcserver.start()
		self.grpcserver.wait_for_termination()
	
					
		self.initialized 	= True
		self.log.info ( ".init [ complete. ] \\\\" )
		
		return True

	
	
	def startinterfaces ( self, ) :
		"""#######################################################################
    
    	Valet's main interface for the user, here the user can ask questions and
    	receive terminal responses from valet on a command line interface - 
    	interactive console session.
    	
    	SensoryCortex | Initialize the Interactive Command Prompt that 
		is Valet's backbone.  All commands will bet sent to this CLI -
		here all other input sensors are initialized.
    		    
	    #######################################################################
	    """
	    
		if not self.commandlineinterface :
		
			self.commandlineinterface = CommandLineInterface ( )
			self.commandlineinterface.instantiate ( self, )	
		
		self.commandlineinterface.cmdloop ( )


	
	def __configure ( self, **kwargs, ) -> bool :
		"""#######################################################################
    
    	Perform any initial setup needed for Valet to operate prior to setting-up
    	the Valet components and microservices, copy kwargs to instance
    	
    	Returns / bool > signifying completion
	    
	    #######################################################################
		"""
					
		###################################################################
		#
		## 	Copy kwargs onto the class instance allowing valet to be
		#	populated with instance variables from passed kwargs
		#
		###################################################################
		self.__dict__.update ( kwargs )
		
		###################################################################
		#
		## 	Iterate the conf directory and load any conf/ini file to an
		#	accessible instance variable using configparser, all loaded
		#	configs get placed in self.configurations.pool[x]
		#
		###################################################################
		self.ini			= Configure ( '.conf', '.ini' )
		self.dbpath			= os.path.join ( self.ini.pool['db']['main']['locale'], 
											self.ini.pool['db']['main']['file'],
											)

		###################################################################
		#
		## 	Setup the Environment for valet to run including logging,
		#	any directories or temporary file architectures for runtime,
		#	any boottime-sanity checks
		#
		###################################################################
		self.environment 	= Environment ( self, )
		self.log 			= self.environment.setuplog ( )
		
		
		###################################################################
		#
		## 	Initalize the google RPC (Protocol Buffer) server to host
		#	concurrent microservices within Valet, to be initialized
		#	during .initialize() on designated server & port
		#
		###################################################################
		self.grpcserver = grpc.server( futures.ThreadPoolExecutor ( 
											max_workers = int ( self.ini.pool['valet']['main']['workers'] ) 
										)
									)		
		self.grpcserver.add_insecure_port ('%s:%s' % (self.ini.pool['valet']['protobuf']['server'], 
												 int ( self.ini.pool['valet']['protobuf']['port'] )  )
											) #('[::]:50051')
		
    	
		###################################################################
		#
		## 	Override the __setattr__ method, telling valet to use the
		#	specified method when a instance property gets changed and
		#	valet.__setattr__ gets called - position at the end of setup
		#	to avoid being called for each of the configuration setup
		#	items here.  We need this to be called during the cortex 
		#	invocations 
		#
		###################################################################
		self.__class__.__setattr__ = self.__broadcast__
		

		self.preinitialized = True
		self.log.info ( ".pre_init [ complete. ] \\\\" )

	
		
	def __broadcast__( self, item, value, ) -> bool :
		"""###################################################################
		
		Broadcast is called upon each Valet class attribute change to the
		Valet.__dict__ object, specified in: 
		
			> self.__class__.__setattr__ = self.__broadcast__
		
		Returns / bool > signifying completion
		
		###################################################################
		"""
		
		self.__dict__ [ item ] = value
		
		###################################################################
		#
		## 	For any assigned object attribute within Valet, check it's 
		#	'listening' property and update object.valet where true. This
		#	ensures all listening sub objects of Valet have up-to-date
		#	valet object references for work at all times 
		#
		###################################################################
		for item in self.__dict__ :
		
			if hasattr ( item, 'listen', )  and item [ 'listen' ] and hasattr ( item, 'valet', ) :
				
				item [ 'valet' ] = self
				
		return True

