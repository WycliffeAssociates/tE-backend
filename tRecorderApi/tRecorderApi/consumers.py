import json

from django.http import HttpResponse
from channels import Group
from channels.handler import AsgiHandler


def http_consumer(message):
    response = HttpResponse('Welcome translation Exchange! You should try websockets.')

    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)

# Register the new client
def ws_add(message):
    Group('game').add(message.reply_channel)
    message.reply_channel.send({
        'text': 'hello',
    })


# Compute a new life’s generation
def ws_receive(message):

    for number in range(1, 101):
        Group('game').send({
            'text': json.dumps({
             'username': 'Juan',
             'is_logged_in': True
             }),
        })


#  Unregister the client for updates
def ws_disconnect(message):
    Group('game').discard(message.reply_channel)
