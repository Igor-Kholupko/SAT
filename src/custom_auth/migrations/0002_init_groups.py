from django.db import migrations
from custom_auth.consts import GROUP_PERMISSIONS


def forwards_func(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Group = apps.get_model('custom_auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model("contenttypes", "ContentType")
    for group, permissions in GROUP_PERMISSIONS.items():
        new_group, created = Group.objects.using(db_alias).get_or_create(name=group)
        for permission in permissions:
            content_type, _ = ContentType.objects.using(db_alias).get_or_create(
                app_label=permission['app'],
                model=permission['model']
            )
            permission_object, created = Permission.objects.using(db_alias).get_or_create(
                codename=permission['codename'],
                name=permission['name'],
                content_type=content_type
            )
            new_group.permissions.add(permission_object)


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('custom_auth', '0001_initial'),
        ('contenttypes', '__latest__'),
    ]

    operations = [
        # OPTIMIZED
        # migrations.RunPython(
        #     code=forwards_func,
        #     reverse_code=reverse_func,
        # ),
    ]
