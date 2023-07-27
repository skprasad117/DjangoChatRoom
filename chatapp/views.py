from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import ChatRoom
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
   
    print("type of ",type(roomname),roomname.isnumeric())
    print("roomname -----:", roomname)
    users = User.objects.all()
    context = {"users":users,"roomname":roomname}
    return render(request,"chatapp/chat.html", context)