class LocalAssistant:
	"""
	Class for example calls to the assistant if IBM services are down.

	Attributes:
		intent (str): the intent of the user's most recent message.
		_intents (dict): a dict of intents to be returned based on input keys
		_messages (dict): a dict of messages to be returned based on user intent
	"""

	def __init__(self):
		self.intent = ""
		self._intents = self._init_intents()
		self._messages = self._init_messages()

	def message(self, msg):
		"""
		Send a message to the assistant, return a list of responses
		:param msg (str): message to be sent
		:return: responses (list) a list of responses
		"""
		response = ""
		if msg.lower() in self._intents.keys():
			self.intent = self._intents[msg.lower()]
			if self.intent in self._messages.keys():
				response = self._messages[self.intent]
		else:
			response = "Can you reword your statement? I'm not understanding."
		return response

	def getIntent(self):
		""" Returns (str) most recent intent stored by the assistant """
		return self.intent

	def _init_intents(self):
		return {
			"": 'Welcome',
			"run a new simulation": 'another_simulation',
			"yes": 'confirm_settings',
			"no": 'deny_settings',
			"new simulation": 'New_Simulation',
			"text-based": 'set_text_entry',
			"new orleans": 'NewOrleans',
			"oklahoma city": 'OklahomaCity',
			'specific': 'set_specific',
			'random': 'set_random',
			'hurricane': 'Hurricane',
			'earthquake': 'Earthquake',
			'tornado': 'Tornado',
			'at the end': 'set_end_reports',
			'evacuate the city': 'evacuation',
			'declare a state of emergency': 'StateEmergency',
			'shelter in place': 'ShelterInPlace',
			'apply for state aid': 'StateAid',
			'apply for federal aid': 'FederalAid',
			'wait': 'wait',
			'end simulation': 'end_simulation',
			'another simulation': 'another_simulation',
			'retry simulation': 'retry_simulation'
		}

	def _init_messages(self):
		return {

			'wait': '',
			'Welcome': 'Hello, I am the disaster simulation assistant. What would you like me to perform?',
			"New_Simulation": "What format of input would you like to use?",
			"set_text_entry": "Okay, setting assistant up for text input\nWhat location would you like to simulate?",
			'NewOrleans': 'Okay, setting location for New Orleans, LA\nWould you like to simulate a specific scenario '
			              'or one at random based on the location\'s history?',
			'OklahomaCity': 'Okay, setting location for Oklahoma City, OK.\nWould you like to simulate a specific '
			                'scenario or one at random based on the location\'s history?',
			'set_specific': 'What type of disaster would you like to simulate?',
			'set_random': 'Okay, randomly generating a disaster based on the locations history.\nAt what point in the '
			              'simulation would you like to see reports?',
			'Hurricane': 'Okay, disaster will simulate a hurricane.\nAt what point in the simulation would you like to '
			             'see reports?',
			'Earthquake': 'Okay, disaster will simulate an earthquake.\nAt what point in the simulation would you like '
			              'to see reports?',
			'Tornado': 'Okay, disaster will simulate a tornado.\nAt what point in the simulation would you like to see reports?',
			'set_end_reports': 'Okay, reports will be given at the end.\nSimulation setup complete. Would you like to begin?',
			'confirm_settings': 'Okay, beginning simulation.',
			'deny_settings': 'Okay, restarting simulation setup.\nWhat format of input would you like to use?',
			'end_simulation': 'Would you like to run another simulation, retry the same simulation, or quit the application?',
			'another_simulation': 'Okay, running another simulation.\nWhat format of input would you like to use?',
			'retry_simulation': 'Okay, running simulation again.\nSimulation setup complete. Would you like to begin?'
		}
