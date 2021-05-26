"""inventory_mgmt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'user/', include(('users.urls', 'users'), namespace='users')),
    path(r'',views.index,name='index'),
    path(r'special/',views.special,name='special'),
    path(r'member/<str:uname>',views.member_dashboard,name='member'),
    path(r'logout/', views.user_logout, name='logout'),
    path(r'createrequest/',views.createRequest,name='create_request'),
    path(r'createclub/',views.createClub,name='create_club'),
    path(r'createitem/',views.createItem,name='create_item'),
    path(r'updaterequest/<int:pk>',views.updateReqStatus,name='update_request'),
    path(r'deleteuser/<int:pk>',views.deleteUser,name='delete_user'),
    path(r'admindb',views.admin_db,name='admin_db'),
    path(r'memberdb',views.member_db,name='member_db'),
]
