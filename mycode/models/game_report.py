# -*- coding: utf-8 -*-
from django.db import models
from mycode.models import   game


class Game_club_report(models.Model):
    game = models.ManyToManyField(game.Game,related_name='game+',blank=False,null=False)
    game_clubA = models.ManyToManyField('GameClub',related_name='game_clubA+',blank=False,null=False)
    game_clubB = models.ManyToManyField('GameClub', related_name='game_clubB+', blank=False, null=False)
    price = models.IntegerField("总费用",default=0)
    score = models.CharField("比分",max_length=255,blank=True,null=False)
    temp_score = models.CharField("预比分",max_length=255,blank=True,null=True,default="")
    award = models.CharField('奖品',max_length=255,blank=True,null=True)
    win_club = models.ManyToManyField('GameClub',related_name='game_club_win+',blank=True,null=True)
    success = models.IntegerField(default=0) #0表示成功,1表示失败
    desc = models.CharField('描述',max_length=255, blank=True,null=True)


class game_club_report_images(models.Model):
    game_club_report = models.ManyToManyField(Game_club_report,related_name='game_club_report+',blank=False,null=False)
    image = models.CharField(max_length=255, blank=True, null=True)  # 俱乐部图片
    content = models.CharField("图片介绍", max_length=255, default='')
    url = models.URLField(null=True, blank=True)
    createTime = models.DateField(auto_created=True, auto_now_add=True)  # 创建时间
    game_club = models.ManyToManyField('GameClub', related_name='game_club+', blank=True)  # "",
    user = models.ManyToManyField('Account', related_name='Commond.game_report+', blank=True, null=True)

class game_club_report_commond(models.Model):
    user = models.ManyToManyField('Account', related_name='Commond.game_report+', blank=True, null=True)
    content = models.CharField(max_length=255)
    anonymity = models.IntegerField(default=10)
    rank = models.IntegerField(default=10)#激烈指数
    skillrank = models.IntegerField(default=10)#技能指数
    game_club_report = models.ManyToManyField(Game_club_report, related_name='Tag.user+', blank=True, null=True)