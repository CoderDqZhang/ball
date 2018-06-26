# -*- coding: utf-8 -*-
from django.db import models
from mycode.models import define,account

class Order(models.Model):
    order_id = models.CharField(max_length=255,null = False, blank=False,primary_key=True)
    user = models.ManyToManyField(account.Account,related_name='order_create_user', blank=False, null=False)
    create_time = models.DateTimeField(auto_created=True)
    end_time = models.DateTimeField(auto_created=False,null=True)
    game_report = models.ManyToManyField('Game_club_report', related_name='Game_club_report', blank=True, null=True)
    game_club = models.ManyToManyField('GameClub', related_name='game_club', blank=True, null=True)
    game = models.ManyToManyField('Game', related_name='Game', blank=True, null=True)
    order_title = models.CharField(max_length=255,default='充值',null=False,blank=False)
    order_desc = models.CharField(max_length=255,default='账户充值',null=False,blank=False)
    order_type = models.IntegerField(default=0)
    price = models.IntegerField(default=0,blank=False,null=False)#订单价格
    status = models.IntegerField(default=1,blank=False,null=False)#订单状态
    rate = models.CharField(max_length=255,blank=True,null=True)#订单评价