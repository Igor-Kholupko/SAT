# Generated by Django 2.1.5 on 2019-03-04 22:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0003_auto_20190305_0019'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labs.Discipline')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labs.Task')),
            ],
        ),
    ]