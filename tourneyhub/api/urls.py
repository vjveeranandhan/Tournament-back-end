from user_manager.views import create_user
from django.urls import path, include

urlpatterns = [
    path('create-user/', create_user, name='create_user')
]