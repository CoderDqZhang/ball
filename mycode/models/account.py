# -*- coding: utf-8 -*-
from django.db import models
from mycode.models import define
from django.contrib.auth.models import User

class Account(models.Model):

    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=200)  # 用户名
    age = models.IntegerField(default=0)  # 年龄
    gender = models.IntegerField(choices=define.GENDER, default=0)
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    game_age = models.IntegerField(default=0)
    phone = models.CharField(max_length=11, default='')
    province = models.CharField(max_length=11, default='')
    city = models.CharField(max_length=11, default='')
    location = models.CharField('用户标识', max_length=100, default='default')
    openid = models.CharField(max_length=200, primary_key=True)
    avatar = models.CharField(max_length=200, default='')
    createTime = models.DateField(auto_created=True,auto_now_add=True)

    def __str__(self):
        return self.nickname


class Ball(models.Model):

    name = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=100)

class Game(models.Model):
    game_create_user = models.ManyToManyField(Account,null=True, verbose_name='Account', blank=True)
    game_detail = models.ManyToManyField(Ball,verbose_name='Ball', null=True, blank=True)
    game_createTime = models.DateField(auto_created=True, auto_now_add=True)
    game_location =  models.CharField('场地', max_length=100, default='default')  #场地
    game_location_detail = models.CharField(max_length=200, default='') #场地具体名称
    game_price = models.IntegerField('费用', default=0)  #费用
    game_start_time = models.DateField()
    game_end_time = models.DateField()
    game_referee = models.BooleanField(default=False)
    game_number = models.IntegerField(default=5)

    game_place_condition  = models.CharField('场地条件', max_length=100, default='default')  #场地

    game_user_list = models.ManyToManyField(Account,null=True, verbose_name='Account', related_name='game_id', blank=True)


