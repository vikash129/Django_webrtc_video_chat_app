# Generated by Django 3.2 on 2022-10-26 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_rename_chat_room_user_chat_room_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='chat_room_id',
            new_name='chat_room',
        ),
    ]
