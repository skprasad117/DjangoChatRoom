from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ChatRoom(models.Model):
    roomname = models.CharField(max_length=30)
    messages = models.TextField()

class OnlineUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)