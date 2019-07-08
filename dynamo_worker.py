import boto3
dynamo_client = boto3.resource('dynamodb')
dynamo_client = dynamo_client.Table('thought-storage')


def get_thought(event, context):
    print(event)
    if event['request']['type'] == "LaunchRequest":
        message = build_speech_plain_response("Time to hear what Twitter is thinking!")
        return build_response(message)
    if event['request']['intent']['name'] == "GetThoughtIntent":
        # Fetch a random thought from DynamoDb
        random_thought = find_random_thought()
        message = build_speech_plain_response(random_thought)
        return build_response(message)


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


def find_random_thought():
    # Find a random thought in DynamoDb
    dynamo_response = dynamo_client.query(KeyConditionExpression=Key('id').eq(1))
    if dynamo_response['Items']:
        return dynamo_response['Items'][0]
    else:
        print("No Thoughts found")
        return []
