# coding=utf-8
from rest_framework import serializers
from mycode.models.account import Account,Ball,Game
from rest_framework import routers, serializers, viewsets


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ('nickname','age','gender','weight','height','game_age',
               'phone','province','city','location','openid','avatar','createTime')

