# Generated by Django 2.0.5 on 2018-06-26 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycode', '0012_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameclub',
            name='club_price',
            field=models.IntegerField(default=0),
        ),
    ]
