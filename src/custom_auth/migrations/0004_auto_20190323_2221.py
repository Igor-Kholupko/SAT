# Generated by Django 2.1.5 on 2019-03-23 19:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0003_auto_20190323_2027'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='specialty',
            new_name='speciality',
        ),
    ]