# Generated by Django 2.2 on 2019-04-19 09:59

from django.db import migrations, models
import django.db.models.deletion

from chat.utils import md5


def create_uuids(apps, schema):
    ChatGroup = apps.get_model('chat', 'ChatGroup')

    def refresh_uuid(obj):
        obj.uuid = md5(list(obj.chatmembership_set.all().values_list('member__id', flat=True).order_by('member__id')))
        obj.save()

    any(map(refresh_uuid, ChatGroup.objects.all()))


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chat_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatgroup',
            name='uuid',
            field=models.UUIDField(default='d41d8cd98f00b204e9800998ecf8427e', db_index=True),
        ),
        migrations.AddField(
            model_name='chatmembership',
            name='last_read',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='chat.Message'),
        ),
        migrations.RunPython(create_uuids, lambda x, y: None)
    ]
