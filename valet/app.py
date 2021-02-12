###########################################################################
#
## @file app.py
#
# ----------------------------------------------------------------------- #
###########################################################################

"""Valet, a personal -everything- assistant. 

Usage:
	app.py [-h | --help]
	app.py [-v | --verbose]
	app.py [-t | --testmode]
	app.py [-c | --console]
	app.py --version

Options:
	-h,--help	: show this help message
	-v,--verbose	: display/log more text output
	--version	: show version

	--input	: initial input string (wrapped in quotes)
	-t,--testmode	: initialize in testing-mode (high verbosity)
	-c,--console	: initialize in interactive console mode
				(otherwise stdout/output-log)
"""

###########################################################################

import os, sys, traceback

from docopt import docopt
from pprint import pprint

from utils.core.valet import Valet
#sys.path.append('..')

###########################################################################



if __name__ == "__main__" :

	#######################################################################
	# 
	##	Docopt will check all arguments, and exit with the Usage string 
	#	if they don't pass. If you simply want to pass your own modules 
	#	documentation then use __doc__, otherwise, you would pass another 
	#	docopt-friendly usage string here. You could also pass your own 
	#	arguments instead of sys.argv with: 
	#	\ 	docopt(__doc__, argv=[your, args])
	#
	###################################################################
	docopt_args = docopt ( __doc__, )
	
	

	# $$$$ ------------------ VALET BLOCK ------------------ $$$$ #
	# $$$$ ------------------------------------------------- $$$$ #
	# $$$$ ------------------------------------------------- $$$$ #
	

	valet		= None
	kwargs 		= {	"name"				: 'valet',
					"base"				: os.path.dirname ( os.path.realpath ( sys.argv [ 0 ] ) ),
					"verbose"			: docopt_args [ '-v' ] or docopt_args [ '--verbose' ],
					"testmode"			: docopt_args [ '-t' ] or docopt_args [ '--testmode' ],
					"interfaceenabled"	: docopt_args [ '-I' ] or docopt_args [ '--interface' ],
				}


	###############################################################
	#
	## 	Initialize the main Valet runner.  This is the core object
	#	that valet is based upon - here, the entire program is
	#	initialized.
	#
	###############################################################
	try :
	
		valet = Valet ( **kwargs, )
	
		valet.initialize ( )
	#	valet.startinterfaces ( )





	# $$$$ ------------------------------------------------- $$$$ #
	# $$$$ ------------------------------------------------- $$$$ #
	# $$$$ ---------------- END VALET BLOCK ---------------- $$$$ #

	
	
	###############################################################
	#
	## 	Exit while handling the keyboard interrupt expression,
	#	sometimes requiring additional debugging or cleanup
	#	versus normal execution
	#
	###############################################################
	except KeyboardInterrupt :
	
		if valet and valet.preinitialized :
		
			valet.log.debug ( "EXIT - KEYBOARD INTERRUPT /CTRL+C/" )
			
		SystemExit ( )



	except Exception as e :
	
		try :
			
			valet.log.error ( "ERROR:\n%s" % traceback.format_exc ( ) )
			
		except :
			
			pass 
			
		finally :

			raise e
			
			
	finally :
	
		if valet and valet.preinitialized :
			
			valet.log.info ( ".exiting. \\\\ \n" )
			
		SystemExit ( )

		
