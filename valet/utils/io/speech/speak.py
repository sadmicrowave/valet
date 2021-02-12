###########################################################################
#
## @file Speak.py
#
###########################################################################

import os, sys, datetime

import pyttsx3, hashlib


###########################################################################
#
##   A wrapper for Valet to take give text and convert to speech
#
#    Valet must take the output text generated from executed functions
#	 generate an mp3 file with the output, and run on the provided output
#	 device
#
###########################################################################

class Speak:
	
    ###################################################################
	#
	## 	Set class level variables
	#
	###################################################################
	DIR				= '/data/speech/'
	engine			= None

	#######################################################################
    #
    ##	The constructor of the class
	#
    #	@valet	/ instance of valet itself to interact with main object
    #	@device / object for output device, defaults to standard-out
	#
	#######################################################################
	def __init__ ( self, valet, device=sys.stdout, ) :
		
		self.server	= valet.server
		self.ini 	= valet.ini
		self.db		= valet.db
		
		self.device = device
		
		self.enabled = True if self.ini.pool['valet']['skills']['vocalization'] == 'on' else False
						

	#######################################################################
    #
    ##	Configure the voice and other options related to the speech
    #	engine pyttsx3 with a voice_enabled setter property
    #
    #	@value / value to set enabled to, simply needs to be set to set to
    #			/ and set to true
    #
    #######################################################################
	@property 
	def enabled ( self, ) :
		
		return self.__enabled or False
		

	@enabled.setter
	def enabled ( self, value, ) :
		
		if value == True :

			try :
			
				###########################################################
				#
				##	Setup the engine and change the rate of speed
				#
				###########################################################
				self.engine = pyttsx3.init ( )
				self.engine.setProperty ( 'rate', self.engine.getProperty ( 'rate' ) - 5 )
				self.engine.setProperty( 'voice', 'com.apple.speech.synthesis.voice.daniel' )
							
			except Exception as e :
								
				raise e
				
		self.__enabled = value

	
		
	#######################################################################
    #
    ##	Run the actual file on the output device if provided.  If not,
    # 	use default system os output
    #
    #	@output / st|list > string or list of values to print as output 
    #
    #######################################################################
	def vocalize ( self, output, ) :

		if self.engine and output :
						
			try : 
				self.engine.say( output )
				#self.engine.runAndWait( )
				self.engine.run()
			
			except Exception as e :
				#	If an error is encountered, generate a file with the 
				#	input contents which generated the error for troubleshooting
				file = os.path.join( self.DIR, 'error', self.__generate_temp_file ( output ) )
				self.engine.save_to_file( output, file )
			
		else :
		
			raise Exception( 'Output audio engine not identified' )
		
		
	
	#######################################################################
    #
    ##	Generate a temporary filename for each speech command that comes
    # 	in so the name of the file doesn't conflict or override each time.
    #	Generate a hash string of the input text
    #
    #	@output / st|list > string or list of values to print as output 
    #	Returns: str > filename string
    #
    #######################################################################
	def __generate_temp_file ( self, output=None, ) :
		
		hash_object = hashlib.md5( output.encode('utf-8') )
		return  "%s - %s.mp3" % ( hash_object.hexdigest(), datetime.datetime.now() )
		
		
