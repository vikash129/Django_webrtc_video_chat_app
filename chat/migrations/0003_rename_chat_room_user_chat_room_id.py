# Generated by Django 3.2 on 2022-10-26 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20221027_0143'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='chat_room',
            new_name='chat_room_id',
        ),
    ]
