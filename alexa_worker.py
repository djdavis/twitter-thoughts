import boto3

def build_response(message, session_attributes={}):
    response = dict()
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    response['response'] = {'outputSpeech': message}
    return response


def build_speech_plain_response(body):
    speech = dict()
    speech['type'] = 'PlainText'
    speech['text'] = body
    return speech

