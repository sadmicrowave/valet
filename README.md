
## Valet
Personal .Everything. Bot.  Valet is a deep-machine-learning personal assistant chatbot written in python.

	  ___      ___ ________  ___       _______  _________   
	 |\  \    /  /|\   __  \|\  \     |\  ___ \|\___   ___\ 
	 \ \  \  /  / | \  \|\  \ \  \    \ \   __/\|___ \  \_| 
	  \ \  \/  / / \ \   __  \ \  \    \ \  \_|/__  \ \  \  
	   \ \    / /   \ \  \ \  \ \  \____\ \  \_|\ \  \ \  \ 
	    \ \__/ /     \ \__\ \__\ \_______\ \_______\  \ \__\
	     \|__|/       \|__|\|__|\|_______|\|_______|   \|__|
	
	
	 ---------------------- INSPIRATIONS / SOURCES ------------------------ #
	
	Chatbot 
		https://www.geeksforgeeks.org/voice-assistant-using-python/?ref=rp
		https://www.geeksforgeeks.org/personal-voice-assistant-in-python/?ref=rp
	
	Deep Machine Learning 
		https://soshnikov.com/azure/deep-pavlov-answers-covid-questions/
		https://colab.research.google.com/github/deepmipt/dp_notebooks/blob/master/DP_ODQA.ipynb#scrollTo=wWoVzv9QBYni



### Wireframe
	# ------------------------- LOGIC MAPPING / FLOW ------------------------ #
	| App.py
    |-> Parse Command Line Arguments with DocOpt module
	|-> Valet
	|	|-> Instantiate Exception Handler
	|	|-> Instantiate Environment
	|	|	|-> Instantiate Log(s)
	|	|
	|	|-> Configuration File Parse / Load .ini
	|	|
	|	|-> Instantiate Persistent Database Connection
	|	|-> Instantiate Communicate handler for I/O ops (brocas area)
	|	|-> Instantiate Server (prefrontal cortex)
	|	|-> Instantiate Intelligence
	|	|	|-> Instantiate Ability Manager
	|	|
	|	|-> -I / Instantiate Interactive Console
	|	|	|-> Continuous Loop - Awaiting User Input
	|	|	|	|-> Ability Manager: Pass Ability to ThreadManager / Server
	|	|	|	|	|-> Execute Ability
	|	|	|	|	|-> Execute Ability Callback (if present)
	|	|	|	|	|-> Pass Results to Communication handler
	|	
	|-> End program
	


## Security Vulnerabilities

If you discover a security vulnerability within the Valet application, please submit a GitHub Issue.  All security vulnerabilities will be promptly addressed.

## License

Valet is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).
