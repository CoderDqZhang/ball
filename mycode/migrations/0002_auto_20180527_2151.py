# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycode', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameClub',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('club_slogan', models.CharField(verbose_name='口号', max_length=255, default='')),
                ('club_desc', models.CharField(verbose_name='介绍', max_length=255, default='')),
                ('club_title', models.CharField(verbose_name='介绍', max_length=255, default='')),
                ('club_post', models.ImageField(blank=True, null=True, default='user1.jpg', upload_to='images/club')),
                ('club_grade', models.IntegerField(default=1)),
                ('club_project', models.CharField(verbose_name='项目介绍', max_length=255, default='')),
                ('club_number', models.IntegerField(default=0)),
                ('club_manager', models.ManyToManyField(blank=True, related_name='clue_manager_user', to='mycode.Account')),
                ('club_user', models.ManyToManyField(blank=True, related_name='clue_user', to='mycode.Account')),
                ('user', models.ManyToManyField(blank=True, related_name='club_create_user', to='mycode.Account')),
            ],
        ),

        migrations.AddField(
            model_name='commond',
            name='skillrank',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='commond',
            name='userrank',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='game',
            name='game_latitude',
            field=models.FloatField(verbose_name='经度', max_length=100, default=0.0),
        ),
        migrations.AddField(
            model_name='game',
            name='game_longitude',
            field=models.FloatField(verbose_name='纬度', max_length=100, default=0.0),
        ),
        migrations.AlterField(
            model_name='apointment',
            name='user',
            field=models.ManyToManyField(blank=True, null=True, related_name='game_list_user', to='mycode.Account'),
        ),
    ]
