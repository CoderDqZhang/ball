# -*- coding: utf-8 -*-
# Generated by Django 2.0.4 on 2018-04-12 07:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('createTime', models.DateField(auto_created=True, auto_now_add=True)),
                ('nickname', models.CharField(max_length=200, verbose_name='用户名')),
                ('sign', models.CharField(blank=True, max_length=200, verbose_name='个性签名')),
                ('age', models.IntegerField(default=0, verbose_name='年龄')),
                ('gender', models.IntegerField(choices=[(1, '男'), (2, '女'), (0, '未知')], default=0, verbose_name='性别')),
                ('weight', models.IntegerField(default=0, verbose_name='体重KG')),
                ('height', models.IntegerField(default=0, verbose_name='身高CM')),
                ('game_age', models.IntegerField(default=0, verbose_name='球龄')),
                ('phone', models.CharField(default='', max_length=11, verbose_name='电话')),
                ('province', models.CharField(default='', max_length=255, verbose_name='所在省份')),
                ('city', models.CharField(default='', max_length=255, verbose_name='所在城市')),
                ('location', models.CharField(default='', max_length=100, verbose_name='用户标识')),
                ('openid', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('avatar', models.CharField(default='', max_length=200, verbose_name='头像')),
                ('good_point', models.CharField(blank=True, max_length=200, verbose_name='擅长')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Apointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=100)),
                ('user', models.ManyToManyField(blank=True, null=True, related_name='_apointment_user_+', to='mycode.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Ball',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sub_title', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, default='user1.jpg', null=True, upload_to='images/ball')),
            ],
        ),
        migrations.CreateModel(
            name='Commond',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('tag_user', models.ManyToManyField(blank=True, null=True, related_name='_commond_tag_user_+', to='mycode.Account')),
                ('user', models.ManyToManyField(blank=True, null=True, related_name='_commond_user_+', to='mycode.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_createTime', models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='创建时间')),
                ('game_title', models.CharField(blank=True, default='', max_length=100, verbose_name='标题')),
                ('game_subtitle', models.CharField(blank=True, default='', max_length=100, verbose_name='副标题')),
                ('game_location', models.CharField(default='', max_length=100, verbose_name='场地')),
                ('game_location_detail', models.CharField(default='', max_length=200, verbose_name='场地地点')),
                ('game_price', models.IntegerField(default=0, verbose_name='费用')),
                ('game_start_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='开始时间')),
                ('game_end_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='结束时间')),
                ('game_referee', models.BooleanField(default=False, verbose_name='裁判')),
                ('game_number', models.IntegerField(default=5, verbose_name='球场人数')),
                ('game_place_condition', models.CharField(default='', max_length=100, verbose_name='场地条件')),
                ('game_create_user', models.ManyToManyField(blank=True, related_name='game_create_user', to='mycode.Account')),
                ('game_detail', models.ManyToManyField(blank=True, to='mycode.Ball')),
                ('game_user_list', models.ManyToManyField(blank=True, null=True, related_name='game_list_user', to='mycode.Apointment')),
            ],
        ),
    ]