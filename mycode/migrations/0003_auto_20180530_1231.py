# Generated by Django 2.0.5 on 2018-05-30 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycode', '0002_unreadmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameClubImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createTime', models.DateField(auto_created=True, auto_now_add=True)),
                ('image', models.CharField(blank=True, max_length=255, null=True)),
                ('content', models.CharField(default='', max_length=255, verbose_name='图片介绍')),
                ('url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='game_club',
            field=models.ManyToManyField(blank=True, null=True, related_name='_game_game_club_+', to='mycode.GameClub'),
        ),
        migrations.AddField(
            model_name='game',
            name='game_club_create',
            field=models.IntegerField(default=0, verbose_name='俱乐部创建'),
        ),
        migrations.AddField(
            model_name='game',
            name='game_club_out',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='是否只允许俱乐部成员'),
        ),
        migrations.AddField(
            model_name='gameclub',
            name='club_status',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='gameclub',
            name='club_post',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='gameclub',
            name='club_title',
            field=models.CharField(default='', max_length=255, verbose_name='名称'),
        ),
        migrations.AddField(
            model_name='gameclubimage',
            name='game_club',
            field=models.ManyToManyField(blank=True, related_name='_gameclubimage_game_club_+', to='mycode.GameClub'),
        ),
        migrations.AddField(
            model_name='gameclubimage',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='_gameclubimage_user_+', to='mycode.Account'),
        ),
    ]
