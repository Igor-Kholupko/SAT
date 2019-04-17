import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection

from django.utils import formats, timezone

from chat.models import User, Message
from chat.utils import pair_uuid, md5


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.receiver = None
        self.chat_id = None
        self.receiver_notificator_id = None

    async def connect(self):
        self.user = self.scope['user']
        self.receiver = User.objects.filter(username=self.scope['url_route']['kwargs']['username'])
        if not self.receiver.exists() or self.user.is_anonymous:
            raise DenyConnection
        self.receiver = self.receiver.first()
        self.chat_id = 'chat_%s' % md5(pair_uuid(self.user.id, self.receiver.id))
        self.receiver_notificator_id = 'notificator_%s' % md5(self.receiver.id)
        await self.channel_layer.group_add(self.chat_id, self.channel_name)
        await self._send_chat_notification(action='join')
        await self.channel_layer.group_send('notificator_%s' % md5(self.user.id), {'type': 'notificator_update'})
        await self.accept()
        Message.objects.filter(to_user_id=self.user.id, from_user_id=self.receiver.id).update(read=True)

    async def disconnect(self, close_code):
        if self.chat_id:
            await self._send_chat_notification(action='left')
            await self.channel_layer.group_discard(self.chat_id, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message'].strip()
        if not message:
            return
        ms = Message(message=message, from_user=self.user, to_user=self.receiver)
        ms.save()
        await self.channel_layer.group_send(
            self.chat_id,
            {
                'type': 'chat_message',
                'message': message,
                'message_id': ms.id,
                'from_user': self.user.id,
                'to_user': self.receiver.id,
                'timestamp': formats.time_format(timezone.localtime(ms.timestamp), use_l10n=True)
            }
        )
        await self.channel_layer.group_send(self.receiver_notificator_id, {'type': 'notificator_update'})

    async def chat_message(self, event):
        if self.user.id == event['to_user']:
            Message.objects.filter(id__exact=event['message_id']).update(read=True)
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'inbound': event['to_user'] == self.user.id,
            'outbound': event['to_user'] == self.receiver.id,
            'timestamp': event['timestamp'],
        }))

    async def chat_notification(self, event):
        if event['user_id'] != self.user.id:
            await self.send(text_data=json.dumps({
                'type': event['type'],
                'message': event['action'],
            }))
            if event['action'] == 'join':
                await self._send_chat_notification(action='greeting')

    async def _send_chat_notification(self, action):
        await self.channel_layer.group_send(
            self.chat_id,
            {
                'type': 'chat_notification',
                'action': action,
                'user_id': self.user.id,
            }
        )


class NotificatorConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.notificator_id = None

    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            raise DenyConnection
        self.notificator_id = 'notificator_%s' % md5(self.user.id)
        await self.channel_layer.group_add(self.notificator_id, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if self.notificator_id:
            await self.channel_layer.group_discard(self.notificator_id, self.channel_name)

    async def notificator_update(self, event):
        event['amount'] = len(Message.get_unread_chats(self.user))
        await self.send(text_data=json.dumps(event))
