from user_manager.views import create_user, user_login, user_logout, get_user, update_user
from django.urls import path, include

urlpatterns = [
    path('create-user/', create_user, name='create_user'),
    path('user-login/', user_login, name='user_login'),
    path('user-logout/', user_logout, name='user_logout'),
    path('get-user/', get_user, name='get_user'),
    path('update-user/', update_user, name='update_user')
]