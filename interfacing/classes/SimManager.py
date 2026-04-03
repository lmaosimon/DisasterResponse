from interfacing.classes.Intents.Intents import Intents
from Simulation.Simulation import Simulation
from interfacing.classes.utils import get_assistant
from interfacing.classes.Search import Search
import sys
import random

locations = ['NewOrleans', 'OklahomaCity', 'NewYork', 'LosAngeles', 'set_location']
disasters = ['Hurricane', 'Wildfire', 'Tornado', 'Pandemic', 'Earthquake', 'Random']
actions = ['ShelterInPlace', 'StateEmergency', 'StateAid', 'FederalAid', 'wait', 'evacuation', 'end_simulation']
end_options = ['retry_simulation', 'another_simulation']
sim_restarts = ['another_simulation', 'deny_settings']
action_prompts = ['What would you like to do?', 'What is your course of action?', 'What action would you like to perform?',
                  'What are your orders?']


class SimManager:
	def __init__(self):
		self.myAssistant = get_assistant(type='ibm')
		self.reset = False
		self.intents = Intents()
		self.prev_intent = None
		self.input_type = ""
		self.sim = Simulation()
		self.finder = Search()
		self.startup = True

	def connect(self):
		response = []
		if self.startup:
			rsp = self.myAssistant.message('')
			response.append(rsp[0] + '\n\n' + rsp[1] + '\n\n')
			self.startup = False
		return response


	def send(self, inp):
		response = []

		inp = inp.replace("\n", "")
		inp = inp.replace("\t", "")

		rsp = ""
		intent = ""
		loc = ""
		if self.prev_intent is None or self.prev_intent in sim_restarts:
			intent = "set_location"
			loc = inp
			rsp = self.myAssistant.message("New York")
			self.input_type = self.prev_intent
		else:
			rsp = self.myAssistant.message(inp)
			intent = self.myAssistant.getIntent()

		if is_flow_correct(intent, self.prev_intent):
			proceed = False
			msg, flag = self.intents.pass_intent(intent=intent, sim=self.sim, loc=loc)
			if flag == 1:
				rsp = self.myAssistant.message("backup")
				self.reset = False
				response.append(msg)
				proceed = True

			self.prev_intent = intent
			for s in rsp:
				if s != "\n":
					response.append(s + '\n')
			print(response)
			if proceed:
				self.prev_intent = self.input_type
				response.append(msg)
				return response
			if self.sim.is_complete() and self.reset is False:
				msg, flag = self.sim.get_feedback()
				response.append("END OF SIM\n~~~~~~~~~~\nFEEDBACK:\n")
				for m in msg:
					response.append(m + '\n')
				response.append("\n~~~~~~~~~~\n")
				self.reset = True
				ending = self.send("end simulation")
				for s in ending:
					response.append(s)
			else:
				if msg is not None:
					response.append(msg + '\n')
				if (self.prev_intent in actions or self.prev_intent == 'confirm_settings') and not self.sim.is_complete():
					response.append(random.choice(action_prompts) + '\n')
				print(response)
				self.reset = False
		else:
			for s in rsp:
				if s != "\n":
					response.append(s + '\n')
			print(response)
		return response


def _location(prev_intent):
	return prev_intent == 'set_text_entry' or prev_intent == 'set_voice_entry'


def _confirm(prev_intent):
	return prev_intent in disasters or prev_intent == 'retry_simulation'


def _take_action(prev_intent):
	return prev_intent == 'confirm_settings' or (prev_intent in actions and prev_intent != 'end_simulation')


def is_flow_correct(intent, prev_intent):
	flowing = False
	if intent == 'New_Simulation':
		flowing = prev_intent is None
	elif intent in locations:
		flowing = prev_intent is None or prev_intent in end_options or prev_intent == 'deny_settings'
	elif intent in disasters:
		flowing = prev_intent in locations
	elif intent == 'confirm_settings':
		flowing = _confirm(prev_intent)
	elif intent == 'deny_settings':
		flowing = _confirm(prev_intent)
	elif intent in actions:
		flowing = _take_action(prev_intent)
	elif intent == 'end_simulation':
		flowing = True
	elif intent in end_options:
		flowing = True

	return flowing
