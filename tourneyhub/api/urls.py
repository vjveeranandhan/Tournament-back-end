from user_manager.views import create_user, user_login, user_logout, get_user, update_user
from club.views import register_club, get_club
from tournament.views import register_tournament, get_tournaments
from django.urls import path

urlpatterns = [
    path('create-user/', create_user, name='create_user'),
    path('user-login/', user_login, name='user_login'),
    path('user-logout/', user_logout, name='user_logout'),
    path('get-user/', get_user, name='get_user'),
    path('update-user/', update_user, name='update_user'),

    path('club/', register_club, name='register_club'),
    path('get-club/', get_club, name='get_club'),

    path('register-tournament/', register_tournament, name='register_tournament'),
    path('get-tournament/', get_tournaments, name='get_tournaments')
]