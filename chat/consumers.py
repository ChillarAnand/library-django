def websocket_receive(message):
    text = message.content.get('text')
    if text:
        reply = {'text': 'Received: {}'.format(text)}
        message.reply_channel.send(reply)
