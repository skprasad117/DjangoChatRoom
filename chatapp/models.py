from django.db import models

# Create your models here.
class ChatRoom(models.Model):
    roomname = models.CharField(max_length=30)
    messages = models.TextField()