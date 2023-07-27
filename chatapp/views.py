from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse

from .models import ChatRoom
from channels.db import database_sync_to_async

# Create your views here.
def chatPage(request,roomname=None):
    if not request.user.is_authenticated:
        return redirect("login-user")
    
    if roomname is None:
        roomname = "PublicChatRoom"
    elif roomname is not "PublicChatRoom":
        user_instance = User.objects.get(username=roomname)

        if user_instance.pk > request.user.pk:
            roomname = request.user.username +"-"+ roomname
        elif user_instance.pk < request.user.pk: 
            roomname = roomname +"-"+request.user.username

    roomname_db_instance = ChatRoom.objects.get_or_create(roomname=roomname)
    if roomname_db_instance[0].messages is not None:
            previous_messages = roomname_db_instance[0].messages.split(",")
            for count, element in enumerate(previous_messages):
                previous_messages[count] = element.replace("-",":")
            print("hello this is previoys messages", previous_messages)
    else:
         previous_messages = "No history Found"
    print("all rooms ", ChatRoom.objects.all())

   
    print("type of ",type(roomname),roomname.isnumeric())
    print("roomname -----:", roomname)
    users = User.objects.all()
    context = {"users":users,"roomname":roomname,"history": previous_messages}
    return render(request,"chatapp/chat.html", context)
