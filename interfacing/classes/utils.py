from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from interfacing.classes.Assistant import Assistant
from interfacing.classes.LocalAssistant import LocalAssistant


def get_assistant(type):

    if type == 'ibm':

        # setup authenticator via IAMAuthentication
        authenticator = IAMAuthenticator('W3cZMJ8LiCalnmwL6g8VqDkyCbWyPvd-9ysFujddxMhN')

        # create new assistant instance and get session information
        assistant = AssistantV2(version='2018-09-20', authenticator = authenticator)
        session = assistant.create_session("7b0904b3-a365-4289-a8dd-6f527b18a512").get_result()

        # create myAssistant object to wrap AssistantV2 methods
        return Assistant(assistant, "7b0904b3-a365-4289-a8dd-6f527b18a512", session['session_id'])
    elif type == 'local':
        return LocalAssistant()
