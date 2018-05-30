# Generated by Django 2.0.5 on 2018-05-28 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycode', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnreadMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read_flag', models.IntegerField(default=0)),
                ('message_type', models.IntegerField(default=0)),
                ('message_type_desc', models.CharField(default='申请入群', max_length=255, verbose_name='类型介绍')),
                ('tag_user_openid', models.ManyToManyField(blank=True, related_name='_unreadmessage_tag_user_openid_+', to='mycode.Account')),
                ('unread_club', models.ManyToManyField(blank=True, related_name='_unreadmessage_unread_club_+', to='mycode.GameClub')),
                ('unread_game', models.ManyToManyField(blank=True, related_name='_unreadmessage_unread_game_+', to='mycode.Game')),
                ('user_openid', models.ManyToManyField(blank=True, related_name='_unreadmessage_user_openid_+', to='mycode.Account')),
            ],
        ),
    ]
