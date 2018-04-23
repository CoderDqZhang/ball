# -*- coding: utf-8 -*-
from django.db import models
from mycode.models import define
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.utils import timezone
import datetime
import sys
import importlib
importlib.reload(sys)

class Account(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname = models.CharField('用户名',max_length=200)  # 用户名
    sign = models.CharField('个性签名', max_length=200, blank=True)  # 用户名
    age = models.IntegerField('年龄',default=0)  # 年龄
    gender = models.IntegerField('性别',choices=define.GENDER, default=0)
    weight = models.IntegerField('体重KG',default=0)
    height = models.IntegerField('身高CM',default=0)
    game_age = models.IntegerField('球龄',default=0)
    phone = models.CharField('电话',max_length=11, default='')
    province = models.CharField('所在省份',max_length=255, default='')
    city = models.CharField('所在城市',max_length=255, default='')
    location = models.CharField('用户标识', max_length=100, default='')
    openid = models.CharField(max_length=200, primary_key=True)
    avatar = models.CharField('头像',max_length=200, default='')
    createTime = models.DateField(auto_created=True,auto_now_add=True)
    good_point = models.CharField('擅长',max_length=200, blank=True)

    def __str__(self):
        return self.nickname


class Ball(models.Model):

    name = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/ball',default='user1.jpg', blank=True, null=True)

    def __str__(self):
        return self.name

    def __meta__(self):
        return

class Apointment(models.Model):
    number = models.CharField(max_length=100)
    user = models.ManyToManyField(Account, related_name='game_list_user', blank=True, null=True)




    def __meta__(self):
        return

class Game(models.Model):
    game_create_user = models.ManyToManyField(Account,related_name='game_create_user', blank=True) #"创建用户",
    game_detail = models.ManyToManyField(Ball, blank=True) #"球约类型",
    game_createTime = models.DateTimeField("创建时间",auto_created=True, auto_now_add=True) #"创建时间",
    game_title = models.CharField("标题", max_length=100, default='',blank=True)  # "创建用户",
    game_subtitle = models.CharField("副标题", max_length=100, default='', blank=True)  # "创建用户",
    game_location =  models.CharField("场地", max_length=100, default='')  #"创建用户",
    game_location_detail = models.CharField("场地地点",max_length=200, default='') #"场地地点",
    game_price = models.IntegerField("费用", default=0)  #费用
    game_start_time = models.DateTimeField("开始时间",default=timezone.now) #"开始时间"
    game_end_time = models.DateTimeField("结束时间",default=timezone.now) #"结束时间"
    game_referee = models.BooleanField("裁判",default=False) #"裁判",
    game_number = models.IntegerField("球场人数",default=5) #"球场人数",

    game_place_condition  = models.CharField("场地条件", max_length=100, default='')  #"场地条件",

    game_user_list = models.ManyToManyField( Apointment,related_name='game_list_user',  blank=True, null=True) # "赴约人",




class Commond(models.Model):
    user = models.ManyToManyField(Account, related_name='Commond.user+', blank=True,null=True)
    content = models.CharField(max_length=255)
    rank = models.IntegerField(default=10)
    tag_user = models.ManyToManyField(Account, related_name='Tag.user+', blank=True,null=True)
