# Generated by Django 2.0.5 on 2018-06-20 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycode', '0008_auto_20180615_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='game_club_report_images',
            name='user',
            field=models.ManyToManyField(blank=True, null=True, related_name='_game_club_report_images_user_+', to='mycode.Account'),
        ),
    ]