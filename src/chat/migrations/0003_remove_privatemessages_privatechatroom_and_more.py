# Generated by Django 4.0.4 on 2022-05-24 21:50

import chat.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_remove_privatemessages_receiver_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='privatemessages',
            name='privateChatroom',
        ),
        migrations.AddField(
            model_name='privatemessages',
            name='chatroomname',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='privatemessages',
            name='receiver',
            field=models.ForeignKey(default=1, on_delete=models.SET(chat.models.get_User), related_name='receiver', to='chat.userprofile'),
        ),
        migrations.AddField(
            model_name='privatemessages',
            name='sender',
            field=models.ForeignKey(default=1, on_delete=models.SET(chat.models.get_User), related_name='sender', to='chat.userprofile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='languageKey',
            field=models.CharField(max_length=10),
        ),
        migrations.DeleteModel(
            name='PrivateChatroom',
        ),
    ]
