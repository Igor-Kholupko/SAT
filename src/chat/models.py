from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from functools import reduce

from chat.utils import md5


User = get_user_model()


class ChatGroup(models.Model):

    class NotInChatException(Exception):
        pass

    users = models.ManyToManyField(
        User,
        related_name='chats',
        related_query_name='chat',
        through='ChatMembership',
        through_fields=('group', 'member')
    )
    uuid = models.UUIDField(default=md5(''), editable=True, db_index=True)

    @property
    def messages(self):
        return Message.objects.filter(sender__group=self).order_by('id')

    def member(self, user):
        member = self.chatmembership_set.filter(member=user)
        if not member.exists():
            raise ChatGroup.NotInChatException
        return member.first()

    def chat_with(self, user=None):
        if user:
            return ", ".join(map(str, self.users.exclude(id=user.id)))
        return ", ".join(map(str, self.users.all()))

    def refresh_uuid(self, commit=False):
        self.uuid = md5(
            list(self.chatmembership_set.all().values_list('member__id', flat=True).order_by('member__id')))
        if commit:
            self.save()

    def create_message(self, user, message, read=False):
        member = self.member(user)
        member.update_last_action()
        return Message.objects.create(message=message, sender=self.member(user), read=read)

    @classmethod
    def get_chats_by_user(cls, user):
        return cls.objects.filter(id__in=cls.objects.filter(chatmembership__member=user)).annotate(
            last=models.FilteredRelation('chatmembership', condition=models.Q(chatmembership__member=user)),
            unread=models.Count(
                'chatmembership__message',
                filter=(
                    ~models.Q(chatmembership__member=user)
                    &
                    (
                        models.Q(chatmembership__message__id__gt=models.F('last__last_read_id'))
                        |
                        models.Q(last__last_read_id__isnull=True)
                    )
                )
            ),
            last_action=models.Max('chatmembership__last_action'),
        ).order_by('-last_action')

    @classmethod
    def get_chats_by_users(cls, *users, strict=True, use_uuid=True):
        if strict and use_uuid:
            uuid = cls.make_uuid(*users)
            qs = cls.objects.filter(uuid=uuid)
        else:
            users_amount = len(users)
            if users_amount == 1:
                qs = cls.get_chats_by_user(*users)
            else:
                qs = cls.objects.annotate(count=models.Count('users')).filter(count=users_amount) \
                     if strict else cls.objects.all()
                qs = reduce(lambda qs, user: qs.filter(users=user), users, qs)
        return qs

    @classmethod
    def get_or_create_chat(cls, *users):
        qs = cls.get_chats_by_users(*users, use_uuid=False)
        return qs.first() if qs.exists() else cls.create_chat(*users)

    @classmethod
    def create_chat(cls, *users):
        instance = cls.objects.create(uuid=cls.make_uuid(*users))
        instance.users.add(*users)
        return instance

    @staticmethod
    def make_uuid(*users):
        return md5(list(sorted([user.id for user in users])))


class ChatMembership(models.Model):
    group = models.ForeignKey(ChatGroup, models.CASCADE)
    member = models.ForeignKey(User, models.CASCADE)
    last_action = models.DateTimeField(default=None, null=True, blank=True)
    last_read = models.ForeignKey('Message', models.SET_NULL, null=True, blank=True)

    def update_last_action(self, commit=True):
        self.last_action = now()
        if commit:
            self.save()

    def update_last_read(self, message, commit=True):
        if isinstance(message, int):
            self.last_read_id = message
        else:
            self.last_read = message
        if commit:
            self.save()


class Message(models.Model):
    message = models.TextField()
    read = models.BooleanField(
        default=False
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    sender = models.ForeignKey(
        ChatMembership,
        models.CASCADE,
        related_name='messages',
        related_query_name='message',
    )
