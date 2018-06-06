from mycode.ball_views import account_view, game, game_club,tsl,tencent_im
from django.conf.urls import url
import os
from ball import settings


urlpatterns = [

#TEST
    url('^create_Im/', account_view.create_Im),
    url('^sendermsg',account_view.testsend_msg),
#User
    url('^login/tenim', tsl.verify_sign),
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
    url('^gameclub/image',game_club.get_game_club_images),
  #im
    url('^im/group',tencent_im.get_im_group_id)
]
