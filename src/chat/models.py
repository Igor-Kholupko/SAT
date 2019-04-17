from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    message = models.TextField()
    read = models.BooleanField(
        default=False
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    from_user = models.ForeignKey(
        User,
        models.DO_NOTHING,
        related_name='outbound_messages',
        related_query_name='outbound_message'
    )
    to_user = models.ForeignKey(
        User,
        models.DO_NOTHING,
        related_name='inbound_messages',
        related_query_name='inbound_message'
    )

    @classmethod
    def get_chat_history(cls, *users):
        users_id = [users[0].id, users[1].id]
        return cls.objects.filter(from_user_id__in=users_id, to_user_id__in=users_id).order_by('id')

    @classmethod
    def get_unread_chats(cls, user):
        qs = cls.objects.filter(to_user_id=user.id, read=False).values("from_user__username").order_by('-id')
        result = []
        for sublist in qs:
            for i in sublist.values():
                if i not in result:
                    result.append(i)
        return result

    @classmethod
    def get_chats(cls, user):
        qs = cls.objects.filter(
            models.Q(to_user_id=user.id) | models.Q(from_user_id=user.id)
        ).values("from_user__username", "to_user__username").order_by('read', '-id')
        result = []
        for sublist in qs:
            for i in sublist.values():
                if i != user.username and i not in result:
                    result.append(i)
        return result
