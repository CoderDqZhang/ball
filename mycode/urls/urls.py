from mycode.ball_views import account_view, game
from django.conf.urls import url
import os
from ball import settings


urlpatterns = [
#User
    url('^test/', account_view.test),
    url('^WeChatlogin/',account_view.verify_user),
    url('^updateUserInfo/',account_view.update_user_info),
    url('^getUserInfo/',account_view.get_user_info),
#ball
    url('^ballList/',game.ball_list),
#game
    url('^gameList/',game.game_list),
    url('^gameCreate/',game.game_create),
    url('^gameDetail/',game.game_detail),

]
