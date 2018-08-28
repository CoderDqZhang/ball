# -*- coding: utf-8 -*-
import importlib
import sys
from django.db import models
from mycode.models import  account,game,game_report

importlib.reload(sys)

class GameClub(models.Model):
    user = models.ManyToManyField(account.Account,related_name='club_create_user+', blank=True) #"创建用户",
    club_ball = models.ManyToManyField(game.Ball, blank=True)  # "球约类型",
    club_manager = models.ManyToManyField(account.Account, related_name='clue_manager_user+', blank=True)  # "管理员",
    club_user = models.ManyToManyField(account.Account, related_name='clue_user+', blank=True)  # "用户",
    club_slogan = models.CharField("口号", max_length=255, default='')  #"场地条件",
    club_desc = models.CharField("介绍", max_length=255, default='')  # "俱乐部介绍",
    club_title = models.CharField("名称", max_length=255, default='')  # "俱乐部介绍",
    club_post = models.CharField(max_length=255, blank=True, null=True)#俱乐部图片
    club_grade = models.IntegerField(default=1)#俱乐部等级
    club_project = models.CharField("项目介绍", max_length=255, default='')
    club_number = models.IntegerField(default=0) #人数限制，0为不限制人数
    club_status = models.IntegerField(default=0) #0表示可以允许成员申请，1表示只能通过邀请加入
    club_price = models.IntegerField(default=0)#会费

class UnreadMessage(models.Model):
    user_openid = models.ManyToManyField(account.Account,related_name='unread_create_user+', blank=True) #"创建用户",
    tag_user_openid = models.ManyToManyField(account.Account,related_name='unread_tag_user+', blank=True) #"创建用户",
    read_flag = models.IntegerField(default=0)
    message_type = models.IntegerField(default=0)
    message_type_desc = models.CharField("类型介绍", max_length=255, default='申请入群')
    unread_club = models.ManyToManyField(GameClub,related_name='club_game+', blank=True) #"创建用户",
    unread_game = models.ManyToManyField(game.Game, related_name='game_ball+', blank=True)  # "创建用户",
    price = models.IntegerField(default=0,null=True)
    unread_game_club_report = models.ManyToManyField(game_report.Game_club_report,
                                                     related_name='Game_club_report+', blank=True,null=True)

class GameClubImage(models.Model):
    user = models.ManyToManyField(account.Account,related_name='image_create_user+', blank=True) #"谁上传的",
    game_club = models.ManyToManyField(GameClub,related_name='game_club+', blank=True) #"上传的俱乐部对象",
    image = models.CharField(max_length=255, blank=True, null=True)#俱乐部图片
    content = models.CharField("图片介绍", max_length=255, default='')
    url = models.URLField(null=True,blank=True)
    createTime = models.DateField(auto_created=True, auto_now_add=True)#创建时间