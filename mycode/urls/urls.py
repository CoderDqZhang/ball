from mycode.ball_views import account_view, game, game_club, game_report
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
#game_club
    url('^creategameclub',game_club.create_game_club),
    url('^mygameclub',game_club.my_game_club_list),
    url('^gameclublist',game_club.game_club_list),
    url('^applyclub',game_club.apply_club),
    url('^gameclubstatus',game_club.club_status),
    url('^gamesendgameinvate',game_club.send_game_invate),
    url('^gameclumanager',game_club.apply_club_manager),
    url('^invateclub',game_club.invate_club),
    url('^leavegameclub',game_club.leave_game_club),
    url('^dissolvegameclub',game_club.dissolve_game_club),
    url('^clubgamedetail',game_club.club_game_detail),
    url('^unreadmessage',game_club.unread_message),
    url('^upload/gameclub/image',game_club.upload_game_club_image),
    url('^gameclub/image/',game_club.)
#game_club_report
    url('^gamereport/create/',game_report.create_game_report),
    url('^gamereport/list/',game_report.get_game_club_report_list),
    url('^gamereport/detail/',game_report.get_game_club_detail),

]
