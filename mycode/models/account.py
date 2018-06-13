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


class Commond(models.Model):
    user = models.ManyToManyField(Account, related_name='Commond.user+', blank=True,null=True)
    content = models.CharField(max_length=255)
    anonymity = models.IntegerField(default=10)
    userrank = models.IntegerField(default=10)
    skillrank = models.IntegerField(default=10)
    tag_user = models.ManyToManyField(Account, related_name='Tag.user+', blank=True,null=True)

