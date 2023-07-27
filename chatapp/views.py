from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
# Create your views here.
def chatPage(request,roomname=None):
    if not request.user.is_authenticated:
        return redirect("login-user")
    if roomname is None:
        roomname = "PublicChatRoom"
    print("roomname -----:", roomname)
    users = User.objects.all()
    context = {"users":users,"roomname":roomname}
    return render(request,"chatapp/chat.html", context)