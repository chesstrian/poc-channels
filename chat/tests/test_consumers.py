import json
import re

import pytest
from asgiref.inmemory import ChannelLayer
from channels import Group
from channels.message import Message
from django.contrib.sessions.backends.file import SessionStore

from chat.consumers import ws_connect, ws_receive, ws_disconnect
from chat.models import Room


@pytest.fixture
def message_factory(settings, tmpdir):
    def factory(name, **content):
        channel_layer = ChannelLayer()
        message = Message(content, name, channel_layer)
        settings.SESSION_FILE_PATH = str(tmpdir)
        message.channel_session = SessionStore()

        return message
    return factory


@pytest.mark.django_db
def test_ws_connect(message_factory):
    room = Room.objects.create(name='Test')
    message = message_factory(
        'test',
        path='/chat/' + str(room.id),
        client=['1.2.3.4', 1234],
        reply_channel='test-reply'
    )
    ws_connect(message)

    assert 'test-reply' in message.channel_layer._groups['room-' + str(room.id)]
    assert message.channel_session['room'] == room.id


@pytest.mark.django_db
def test_ws_receive(message_factory):
    room = Room.objects.create(name='Test')
    message = message_factory(
        'test',
        text=json.dumps({'username': 'some', 'message': 'text'})
      )

    # This would happen when the user joins the room.
    message.channel_session['room'] = room.id
    Group('room-' + str(room.id), channel_layer=message.channel_layer).add(u'test-reply')

    ws_receive(message)

    _, reply = message.channel_layer.receive_many([u'test-reply'])
    reply = json.loads(reply['text'])
    assert reply['message'] == 'text'
    assert reply['username'] == 'some'


@pytest.mark.django_db
def test_ws_disconnect(message_factory):
    room = Room.objects.create(name='Test')
    message = message_factory('test', reply_channel=u'test-reply1')
    Group('room-' + str(room.id), channel_layer=message.channel_layer).add(u'test-reply1')
    Group('room-' + str(room.id), channel_layer=message.channel_layer).add(u'test-reply2')
    message.channel_session['room'] = room.id

    ws_disconnect(message)
    assert 'test-reply1' not in message.channel_layer._groups['room-' + str(room.id)]
