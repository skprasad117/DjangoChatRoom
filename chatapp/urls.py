from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", views.chatPage, name="chat-page"),
    path("<str:roomname>/", views.chatPage, name="chat-page"),
 
    # login-section
    path("auth/login/", LoginView.as_view
         (template_name="chatapp/login.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
]