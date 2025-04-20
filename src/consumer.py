def handle(event, context):
    messages = event['Records']

    for message in messages:
        print(message['Records'])
