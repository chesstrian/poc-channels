import json
from datetime import datetime

from channels import Group
from channels.sessions import channel_session


from chat.models import Room
from chat.bot_client import BotClient


@channel_session
def ws_connect(message):
    try:
        prefix, room_id = message['path'].strip('/').split('/')
        room = Room.objects.get(id=room_id)
    except ValueError:
        # Invalid path, someone is trying to hack
        return
    except Room.DoesNotExist:
        # Invalid room id
        return

    Group('room-' + room_id, channel_layer=message.channel_layer).add(message.reply_channel)

    message.channel_session['room'] = room.id


@channel_session
def ws_receive(message):
    try:
        room_id = message.channel_session['room']
        room = Room.objects.get(id=room_id)
    except KeyError:
        # No room in channel_session
        return
    except Room.DoesNotExist:
        # Room might be deleted from DB, for instance
        return

    try:
        data = json.loads(message['text'])
    except ValueError:
        # No message, or invalid message
        return

    if set(data.keys()) != {'username', 'message'}:
        # Unexpected data format
        return

    if data['message'].startswith('/stock=') or data['message'].startswith('/day_range='):
        command, symbol = data['message'].strip('/').split('=')

        bot = BotClient()
        error, text = bot.call(command, symbol)

        data['username'] = 'rob-bot'
        data['message'] = text

        if error:
            data['datetime'] = datetime.now().strftime('%b %-d %-I:%M %p')
            message.reply_channel.send({
                'text': json.dumps(data)
            })
            return

    if data:
        msg = room.history.create(**data)

        Group('room-' + str(room_id), channel_layer=message.channel_layer).send({
            'text': json.dumps(msg.as_dict())
        })


@channel_session
def ws_disconnect(message):
    try:
        room_id = message.channel_session['room']
        Room.objects.get(id=room_id)
        Group('room-' + str(room_id), channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, Room.DoesNotExist):
        pass
