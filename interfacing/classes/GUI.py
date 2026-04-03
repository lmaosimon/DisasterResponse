from interfacing.classes.Intents.Intents import Intents
from Simulation.Simulation import Simulation
from tkinter import Tk, StringVar, Frame, LabelFrame, Label
from tkinter import messagebox, Text, Button, WORD, DISABLED, W, NORMAL, END
from interfacing.classes.Search import Search
import speech_recognition as sr
import sys
import random

locations = ['NewOrleans', 'OklahomaCity', 'NewYork', 'LosAngeles', 'set_location']
disasters = ['Hurricane', 'Wildfire', 'Tornado', 'Pandemic', 'Earthquake', 'Random', 'Invasion', 'Meteor', 'Asteroid', 'Sun_Dissipating']
actions = ['ShelterInPlace', 'StateEmergency', 'StateAid', 'FederalAid', 'wait', 'evacuation', 'end_simulation', 'declare_fealty', 'gather_military', 'recruit_bruce_willis', 'declare_anarchy']
end_options = ['retry_simulation', 'another_simulation']
sim_restarts = ['another_simulation', 'deny_settings']
action_prompts = ['What would you like to do?', 'What is your course of action?', 'What action would you like to perform?',
                  'What are your orders?']
voice_msg = None

class GUI:
	def __init__(self, assistant):
		self.myAssistant = assistant
		self.reset = False
		self.intents = Intents()
		self.prev_intent = None
		self.input_type = ""
		self.sim = Simulation()
		self.finder = Search()
		if not self.finder:
			print('Error setting up location search')

		self._gui_init()

	def _gui_init(self):
		self.tk = Tk()
		self.tk.title('Disaster Response Simulation Assistant')
		self.sim_info = StringVar()

		# Center the initial frame
		self.tk.update_idletasks()
		width = 1000
		height = 400
		x = (self.tk.winfo_screenwidth() // 2) - (width // 2)
		y = (self.tk.winfo_screenheight() // 2) - (height // 2)
		self.tk.geometry('{}x{}+{}+{}'.format(width, height, x, y))

		# Frame Setup
		user_section = Frame(height=800, width=100, bg='light grey')
		f_msglist = Frame(height=400, width=50, bg='light grey')
		f_msgsend = LabelFrame(user_section, text='Input', height=300, width=300, bg='light grey')
		f_floor = Frame(user_section, height=100, width=100, bg='light grey')
		info_frame = LabelFrame(user_section, text='Info', height=400, width=100, bg='light grey')
		current_info = Label(user_section, textvariable=self.sim_info, bd=5, bg='light grey')

		# Text Msg Box Setup
		self.txt_msglist = Text(f_msglist, bd=5, wrap=WORD, width=70)
		self.txt_msglist.tag_config('green', foreground='blue', font=('Courier', 10))
		self.txt_msgsend = Text(f_msgsend, height=5, width=50, bd=5, wrap=WORD)
		self.txt_msglist.config(state=DISABLED)

		# Button setup
		button_send = Button(f_floor, text='Send', command=self.msgsend, bg='grey')
		button_clear = Button(f_floor, text='Clear', command=self.clear, bg='grey')
		button_help = Button(f_floor, text='Help', command=self.help, bg='grey')
		button_voice = Button(f_floor, text='Voice Input', command=self.voice, bg='grey')

		# Info label setup
		actions_info_label = Label(info_frame, text="Actions", fg='red', bg='light grey')
		actions_info = Label(info_frame, text='Wait: Advance the simulation by one step.\nDeclare Emergency: Declare '
		                                      'a state of emergency in the city.\nApply for Federal Aid: Apply for '
		                                      'financial help from the federal government.\nApply for State Aid: '
		                                      'Apply for financial help from the state government.\nOrder Evacuation: '
		                                      'Order the citizens of the city to evacuate.\nOrder Shelter in Place: '
		                                      'Order the citizens to stay in their current locations.', justify="left", bg='light grey')
		disaster_info_label = Label(info_frame, text='Disasters', fg='red', bg='light grey')
		disaster_info = Label(info_frame, text="Hurricane, Tornado, Pandemic, Wildfire, Earthquake, Random", anchor=W,
							  justify="left", bg='light grey')

		# Grid layout setup
		user_section.grid(row=0, column=0)
		info_frame.grid(row=0, column=0)
		current_info.grid(row=1, column=0)
		f_msglist.grid(row=0, column=1)
		f_msgsend.grid(row=3, column=0)
		f_floor.grid(row=4, column=0)
		actions_info_label.grid(row=0, column=0)
		actions_info.grid(row=1, column=0)
		disaster_info_label.grid(row=4, column=0)
		disaster_info.grid(row=5, column=0)
		user_section.grid_rowconfigure(4, minsize=70)  # Here
		self.txt_msglist.grid(row=0, column=1)
		self.txt_msgsend.grid()
		button_send.grid(row=0, column=0, sticky=W)
		button_clear.grid(row=0, column=1, sticky=W)
		button_help.grid(row=0, column=2, sticky=W)
		button_voice.grid(row=0, column=3, sticky=W)

		# Keyboard binds setup
		self.tk.bind('<Escape>', self.close)
		self.tk.bind('<Return>', self.msgsendEvent)

		# Beginning of sim msg
		self.txt_msglist.config(state=NORMAL)
		rsp = self.myAssistant.message('')
		self.txt_msglist.insert(END,
		                        rsp[0] + '\n\n' + rsp[1] + '\n\n', 'green')
		self.txt_msglist.config(state=DISABLED)

		self.tk.mainloop()

	def msgsend(self):
		self.txt_msglist.yview(END)
		self.txt_msglist.config(state=NORMAL)

		global voice_msg
		if voice_msg != None:
			inp = voice_msg
			# Reset the voice_msg.
			voice_msg = None

		else:
			inp = self.txt_msgsend.get('0.0', END)
			inp = inp.replace("\n", "")
			inp = inp.replace("\t", "")

		if inp != 'end simulation':
			self.txt_msglist.insert(END, inp + '\n')

		rsp = ""
		intent = ""
		loc = ""
		if self.prev_intent is None or self.prev_intent in sim_restarts:  # do location searching here
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
				self.txt_msgsend.delete('0.0', END)
				self.txt_msglist.insert(END, msg + '\n', 'green')
				proceed = True

			self.sim_info.set(f"CURRENT SIMULATION: LOCATION: {self.sim.location}, DISASTER: {self.sim.disaster}")
			self.prev_intent = intent
			for s in rsp:
				self.txt_msglist.insert(END, s + '\n', 'green')
			if proceed:
				self.prev_intent = self.input_type
				return
			if self.sim.is_complete() and self.reset is False:
				msg, flag = self.sim.get_feedback()
				self.txt_msgsend.delete('0.0', END)
				self.txt_msgsend.insert(END, "end simulation")
				self.txt_msglist.insert(END, "END OF SIM\n~~~~~~~~~~\nFEEDBACK:\n", 'green')
				for m in msg:
					self.txt_msglist.insert(END, m + '\n', 'green')
				self.txt_msglist.insert(END, "\n~~~~~~~~~~\n", 'green')
				self.reset = True
				self.msgsend()
			else:
				if msg is not None:
					self.txt_msglist.insert(END, msg + '\n', 'green')
				if (self.prev_intent in actions or self.prev_intent == 'confirm_settings') and not self.sim.is_complete():
					self.txt_msglist.insert(END, random.choice(action_prompts) + '\n', 'green')
				self.reset = False
				self.txt_msgsend.delete('0.0', END)


		else:
			if type(rsp) == list:
				for s in rsp:
					self.txt_msglist.insert(END, s + '\n', 'green')
			elif type(rsp) == str:
				self.txt_msglist.insert(END, rsp + '\n', 'green')
			self.txt_msgsend.delete('0.0', END)

		self.previous_response = rsp
		self.txt_msglist.insert(END, '\n', 'green')
		self.txt_msglist.config(state=DISABLED)

	def close(self, event):
		self.tk.withdraw()
		sys.exit()

	def msgsendEvent(self, event):
		if event.keysym == 'Return':
			self.msgsend()

	def clear(self):
		self.txt_msgsend.delete('0.0', END)

	def help(self):
		messagebox.showinfo('Help', 'Available Actions:\nWait\nApply for Federal Aid\nApply for State Aid\nOrder '
		                            'Shelter in Place\nOrder Evacuation\nDeclare Emergency')

	def voice(self):
		# Make recognizer instances.
		r = sr.Recognizer()
		with sr.Microphone() as source:
			audio = r.listen(source)
			try:
				global voice_msg
				voice_msg = r.recognize_google(audio)
				self.msgsend()
			except:
				voice_msg = 'Sorry, I could not recognize your words.'
				self.msgsend()

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
	else:   # Default to just going with the flow
		flowing = True

	return flowing

