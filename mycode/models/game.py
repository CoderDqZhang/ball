# -*- coding: utf-8 -*-
import importlib
import sys
from django.db import models
from django.utils import timezone
from mycode.models import  account

importlib.reload(sys)

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
    user = models.ManyToManyField(account.Account, related_name='game_list_user', blank=True, null=True)

    def __meta__(self):
        return

class Game(models.Model):
    game_create_user = models.ManyToManyField(account.Account,related_name='game_create_user', blank=True) #"创建用户",
    game_detail = models.ManyToManyField(Ball, blank=True) #"球约类型",
    game_createTime = models.DateTimeField("创建时间",auto_created=True, auto_now_add=True) #"创建时间",
    game_title = models.CharField("标题", max_length=100, default='',blank=True)  # "创建用户",
    game_subtitle = models.CharField("副标题", max_length=100, default='', blank=True)  # "创建用户",
    game_location =  models.CharField("场地", max_length=100, default='')  #"创建用户",
    game_latitude = models.FloatField('经度',max_length=100,default=0.0)
    game_longitude = models.FloatField('纬度', max_length=100, default=0.0)
    game_location_detail = models.CharField("场地地点",max_length=200, default='') #"场地地点",
    game_price = models.IntegerField("费用", default=0)  #费用
    game_start_time = models.DateTimeField("开始时间",default=timezone.now) #"开始时间"
    game_end_time = models.DateTimeField("结束时间",default=timezone.now) #"结束时间"
    game_referee = models.BooleanField("裁判",default=False) #"裁判",
    game_number = models.IntegerField("球场人数",default=5) #"球场人数",

    game_place_condition  = models.CharField("场地条件", max_length=100, default='')  #"场地条件",

    game_user_list = models.ManyToManyField( Apointment,related_name='game_list_user',  blank=True, null=True) # "赴约人",

    #增加俱乐部控制
    game_club_create = models.IntegerField("俱乐部创建", default=0)  # "场地条件",0表示非俱乐部成员创建,1表示俱乐部内部，2表示俱乐部对抗赛
    game_club = models.ManyToManyField('GameClub', related_name='game_club+', null=True, blank=True)
    game_club_out = models.IntegerField('是否只允许俱乐部成员', blank=True, null=True, default=0)  # 0表示可以允许平台所有用户加入