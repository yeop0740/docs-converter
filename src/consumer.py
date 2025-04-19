def handle(event):
    messages = event['Records']

    for message in messages:
        print(message['Records'])

