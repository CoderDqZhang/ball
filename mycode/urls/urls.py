from mycode.ball_views import account_view, game
from django.conf.urls import url

urlpatterns = [
#User
    url('^test/', account_view.test),
    url('^WeChatlogin/',account_view.verify_user),
#ball
    url('^ball_list/',game.ball_list),
#game
    url('^game_list/',game.game_list)
]
