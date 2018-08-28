# -*- coding: utf-8 -*-
import importlib
import sys
from django.contrib.auth.models import User
from django.db import models
from mycode.models import define

importlib.reload(sys)

class Account(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname = models.CharField('用户名',max_length=200)  # 用户名
    sign = models.CharField('个性签名', max_length=200, blank=True,null=True)  # 用户名
    age = models.IntegerField('年龄',default=0,null=True)  # 年龄
    gender = models.IntegerField('性别',choices=define.GENDER, default=0,null=True)
    weight = models.IntegerField('体重KG',default=0,null=True)
    height = models.IntegerField('身高CM',default=0,null=True)
    game_age = models.IntegerField('球龄',default=0,null=True)
    phone = models.CharField('电话',max_length=11, default='',null=True)
    province = models.CharField('所在省份',max_length=255, default='',null=True)
    city = models.CharField('所在城市',max_length=255, default='',null=True)
    location = models.CharField('用户标识', max_length=100, default='',null=True)
    openid = models.CharField(max_length=200, primary_key=True)
    avatar = models.CharField('头像',max_length=200, default='',null=True)
    createTime = models.DateField(auto_created=True,auto_now_add=True)
    good_point = models.CharField('擅长',max_length=200, blank=True,null=True)
    balance = models.FloatField('余额',max_length=255,blank=True,null=True)


    def __str__(self):
        return self.nickname


class Commond(models.Model):
    user = models.ManyToManyField(Account, related_name='Commond.user+', blank=True,null=True)
    content = models.CharField(max_length=255)
    anonymity = models.IntegerField(default=10)
    userrank = models.IntegerField(default=10)
    skillrank = models.IntegerField(default=10)
    tag_user = models.ManyToManyField(Account, related_name='Tag.user+', blank=True,null=True)

class IM(models.Model):
    game = models.OneToOneField('Game',related_name='game_im+', blank=True,null=True,on_delete=models.CASCADE)
    game_club = models.OneToOneField('GameClub', related_name='game_club_im+', blank=True, null=True,on_delete=models.CASCADE)
    room = models.CharField("群id", max_length=255)
    createTime = models.DateField(auto_created=True, auto_now_add=True)  # 创建时间


class TopUp(models.Model):
    price = models.IntegerField()

