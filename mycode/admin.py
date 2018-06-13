from django.contrib import admin

from mycode.models.account import Account,Commond
from mycode.models.game import Game, Ball
from mycode.models.game_club import GameClub


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'age', 'openid', 'gender', 'city', 'province','weight',
                    'height','game_age','phone','avatar','createTime')

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ( 'game_location', 'game_location_detail',
                    'game_price', 'game_start_time','game_end_time',
                    'game_referee','game_number','game_place_condition'
                    )

@admin.register(Ball)
class BallAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_title',)

@admin.register(Commond)
class CommondAdmin(admin.ModelAdmin):
    list_display = ('content',)

@admin.register(GameClub)
class CommondAdmin(admin.ModelAdmin):
    list_display = ('club_slogan','club_desc'
                    ,'club_title','club_post','club_grade','club_project','club_number')
