from django.contrib.auth.models import User
from .models import ChatRoom, OnlineUsers


def upadte_and_get_user_status_list():
    users_instance =  User.objects.all()
    response_data = dict
    for user in users_instance:
        OnlineUsers.objects.get_or_create(user=user)
    return None