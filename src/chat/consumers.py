import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection

from django.utils import formats, timezone

from chat.models import Message, ChatGroup


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.chat_group = None
        self.chat_id = None
        self.notificator_id = None

    async def connect(self):
        self.user = self.scope['user']
        self.chat_group = ChatGroup.get_chats_by_user(self.user).filter(uuid=self.scope['url_route']['kwargs']['uuid'])
        if not self.chat_group.exists():
            raise DenyConnection
        else:
            self.chat_group = self.chat_group.first()
        self.chat_id = 'chat_%s' % self.chat_group.uuid
        self.notificator_id = 'notificator_%s' % self.chat_group.uuid

        await self.channel_layer.group_add(self.chat_id, self.channel_name)
        await self._send_chat_notification(action='join')
        await self.accept()

        mqs = self.chat_group.messages
        mqs.update(read=True)
        self.chat_group.member(self.user).update_last_read(mqs.first())

    async def disconnect(self, close_code):
        if self.chat_id:
            await self._send_chat_notification(action='left')
            await self.channel_layer.group_discard(self.chat_id, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message'].strip()
        if not message:
            return
        ms = self.chat_group.create_message(self.user, message)
        await self.channel_layer.group_send(
            self.chat_id,
            {
                'type': 'chat_message',
                'message': message,
                'message_id': ms.id,
                'from_user': self.user.id,
                'timestamp': formats.time_format(timezone.localtime(ms.timestamp), use_l10n=True)
            }
        )
        await self.channel_layer.group_send(self.notificator_id, {'type': 'notificator_update'})

    async def chat_message(self, event):
        if self.user.id != event['from_user']:
            Message.objects.filter(id=event['message_id']).update(read=True)
            self.chat_group.member(self.user).update_last_read(event['message_id'])
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'outbound': event['from_user'] == self.user.id,
            'inbound': event['from_user'] != self.user.id,
            'timestamp': event['timestamp'],
        }))

    async def chat_notification(self, event):
        if event['user_id'] != self.user.id:
            await self.send(text_data=json.dumps(event))
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
        self.notificator_ids = []

    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            raise DenyConnection
        self.notificator_ids = ChatGroup.get_chats_by_user(self.user).values_list('uuid', flat=True)

        for notificator_id in self.notificator_ids:
            await self.channel_layer.group_add('notificator_%s' % notificator_id, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if self.notificator_ids:
            for notificator_id in self.notificator_ids:
                await self.channel_layer.group_discard('notificator_%s' % notificator_id, self.channel_name)

    async def notificator_update(self, event):
        event['amount'] = ChatGroup.get_chats_by_user(self.user).exclude(unread=0).count()
        await self.send(text_data=json.dumps(event))
