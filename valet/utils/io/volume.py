###########################################################################
#
## @file volume.py
#
###########################################################################

import volux

#from voluxcliprint import VoluxCliPrint
#from voluxaudio import VoluxAudio
#from voluxGui import VoluxGui

###########################################################################
#
##   A wrapper for Valet to interface with the volume of the system
#
#    This is helpful when querying system volume levels or setting. This
#	 will also be used as the general interface to device volume controls
#	 later when other configurable devices are connected
#
###########################################################################

class Volume :
    #######################################################################
    #
    ##	The constructor of the class
    #
    #######################################################################
	def __init__ ( self, input=None ) :
		self.input = input

		self.vlx = volux.VoluxOperator()
		
		print( 'vlx: %s' % self.vlx )
	