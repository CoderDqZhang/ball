from django.contrib import admin

from mycode.models.account import Account, Game, Ball


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
    # 'createTime',
    # def createTime(self, obj):
    #     if obj.game_detail is None:
    #         print("dsf")
    #         return ""
    #     else:
    #         print(obj.game_detail)
    #         for p in obj.game_create_user.all():
    #             print(p)
    #         return "\n".join([p.nickname for p in obj.game_create_user.all()])
    # def createTime(self, obj):
    #     print(obj.game_create_user.nickname)
    #     return obj.game_create_user.nickname

    # createTime.admin_order_field = 'createTime'
    #
    # def gameDetail(self, obj):
    #     return obj.game_detail.name
    # def userList(self, obj):
    #     return obj.game_user_list.nickname
    #
    # userList.admin_order_field = 'userList'

@admin.register(Ball)
class BallAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_title')
