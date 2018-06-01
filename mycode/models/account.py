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
from django.db.models import Q

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
    game_club_create = models.IntegerField("俱乐部创建", default=0)  # "场地条件",0表示非俱乐部成员创建
    game_club = models.ManyToManyField('GameClub', related_name='game_club+', null=True, blank=True)
    game_club_out = models.IntegerField('是否只允许俱乐部成员', blank=True, null=True, default=0)  # 0表示可以允许平台所有用户加入


class Commond(models.Model):
    user = models.ManyToManyField(Account, related_name='Commond.user+', blank=True,null=True)
    content = models.CharField(max_length=255)
    anonymity = models.IntegerField(default=10)
    userrank = models.IntegerField(default=10)
    skillrank = models.IntegerField(default=10)
    tag_user = models.ManyToManyField(Account, related_name='Tag.user+', blank=True,null=True)


class GameClub(models.Model):
    user = models.ManyToManyField(Account,related_name='club_create_user+', blank=True) #"创建用户",
    club_ball = models.ManyToManyField(Ball, blank=True)  # "球约类型",
    club_manager = models.ManyToManyField(Account, related_name='clue_manager_user+', blank=True)  # "管理员",
    club_user = models.ManyToManyField(Account, related_name='clue_user+', blank=True)  # "用户",
    club_slogan = models.CharField("口号", max_length=255, default='')  #"场地条件",
    club_desc = models.CharField("介绍", max_length=255, default='')  # "俱乐部介绍",
    club_title = models.CharField("名称", max_length=255, default='')  # "俱乐部介绍",
    club_post = models.CharField(max_length=255, blank=True, null=True)#俱乐部图片
    club_grade = models.IntegerField(default=1)#俱乐部等级
    club_project = models.CharField("项目介绍", max_length=255, default='')
    club_number = models.IntegerField(default=0) #人数限制，0为不限制人数
    club_status = models.IntegerField(default=0) #0表示可以允许成员申请，1表示只能通过邀请加入

class UnreadMessage(models.Model):
    user_openid = models.ManyToManyField(Account,related_name='unread_create_user+', blank=True) #"创建用户",
    tag_user_openid = models.ManyToManyField(Account,related_name='unread_tag_user+', blank=True) #"创建用户",
    read_flag = models.IntegerField(default=0)
    message_type = models.IntegerField(default=0)
    message_type_desc = models.CharField("类型介绍", max_length=255, default='申请入群')
    unread_club = models.ManyToManyField(GameClub,related_name='club_game+', blank=True) #"创建用户",
    unread_game = models.ManyToManyField(Game, related_name='game_ball+', blank=True)  # "创建用户",

class GameClubImage(models.Model):
    user = models.ManyToManyField(Account,related_name='image_create_user+', blank=True) #"谁上传的",
    game_club = models.ManyToManyField(GameClub,related_name='game_club+', blank=True) #"上传的俱乐部对象",
    image = models.CharField(max_length=255, blank=True, null=True)#俱乐部图片
    content = models.CharField("图片介绍", max_length=255, default='')
    url = models.URLField(null=True,blank=True)
    createTime = models.DateField(auto_created=True, auto_now_add=True)#创建时间

class IM(models.Model):
    game = models.OneToOneField(Game,related_name='game_im+', blank=True,null=True,on_delete=models.CASCADE)
    game_club = models.OneToOneField(GameClub, related_name='game_club_im+', blank=True, null=True,on_delete=models.CASCADE)
    room = models.CharField("群id", max_length=255)
    createTime = models.DateField(auto_created=True, auto_now_add=True)  # 创建时间