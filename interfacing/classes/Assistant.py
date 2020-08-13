
class Assistant:
    """Class for simple calls for the UI

    Attributes: 
        assistant_inst (AssistantV2): AssistantV2 object that will call the API
        assistant_id (str): The user's assistant ID used for calling
        session_id (str): The session ID created with the AssistantV2 object
        intent (str): The intent of the user's most recent message

    """
    assistant_inst = None
    assistant_id = ""
    session_id = ""
    intent = ""

    def __init__(self, assistant, a_id, s_id):
        """ Pass in the  assistant object, its ID, and its sessionID

        Args:
            assistant (AssistantV2): AssistantV2 object
            a_id (str): Assistant ID of the assistant object passed
            s_id (str): Session ID for the assistant object passed

        """
        self.assistant = assistant
        self.assistant_id = a_id
        self.session_id = s_id

    def message(self, msg):
        """ Send a message to the assistant, return a list of responses

        Args:
            msg (str): Message to send to the assistant
        
        """
        response_json = self.assistant.message(self.assistant_id, self.session_id, input={'text': msg}, context={'metadata': {'deployment': 'myDeployment'}}).get_result()

        # set most likely recent intent
        intents = response_json['output']['intents']
        if len(intents) > 0:
            self.intent = intents[0]['intent']

        responses = []
        for rsp in response_json['output']['generic']:
            if rsp['response_type'] == 'text':
                responses.append(rsp['text'])
        
        return responses
    
    def getIntent(self):
        """ Returns (str) most recent intent stored by the assistant and removes it"""
        intent = self.intent
        self.intent = None
        return intent


