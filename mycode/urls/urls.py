from mycode.ball_views import account_view, game
from django.conf.urls import url
import os
from ball import settings


urlpatterns = [
#User
    url('^test/', account_view.test),
    url('^wechatlogin/',account_view.verify_user),
    url('^updateuserinfo/',account_view.update_user_info),
    url('^getuserinfo/',account_view.get_user_info),
    url('^commond/',account_view.conmmend_user),
    url('^usercommond/',account_view.get_user_conmmend),
    url('^userothercommond/',account_view.get_user_other_conmmend),
#ball
    url('^balllist/',game.ball_list),
#game
    url('^gamelist/',game.game_list),
    url('^gamecreate/',game.game_create),
    url('^gamedetail/',game.game_detail),
    url('^gameappointment/',game.game_appointment),
    url('^mygameappoinment/',game.my_game_appointment),
    url('^gamecancelappoinment/',game.cancel_game_appointment),
    url('^gamesearch/',game.search),
    url('^gamedelete/',game.delete_my_game_appointment),

]
