# Generated by Django 2.0.5 on 2018-06-13 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycode', '0003_auto_20180530_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='unreadmessage',
            name='price',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
