from django.urls import path
from django.http import HttpRequest

from . import views


urlpatterns =[
    path('login/',views.loginpage,name="loginpage"),
    path('logout/',views.logoutuser,name="logoutuser"),
    path('register/',views.registeruser,name="registeruser"),
    path("",views.homepage,name="homepage"),
    path("userprofile/<str:pk>/",views.userprofile,name="userprofile"),
    path("chatroom/<str:pk>/",views.chatroom,name="chatroom"),
    path("chatroom_form/",views.chatroomform,name="chatroomform"),
    path("editchatroom/<str:pk>/",views.editchatroom,name="editchatroom"),   
    path("deletechatroom/<str:pk>/",views.deletechatroom,name="deletechatroom"),
    path("deletemessage/<str:pk>/",views.deletemessage,name="deletemessage"),
    path("updateuser",views.updateuser,name="updateuser"),

    

]
