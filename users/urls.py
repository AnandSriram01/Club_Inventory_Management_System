
from django.urls import path
from . import views


urlpatterns = [
    path(r'register/',views.register,name='register'),
    path(r'user_login/',views.user_login,name='user_login'),
]
