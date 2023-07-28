import time
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import SyncConsumer

from django.contrib.auth import get_user
from django.contrib.auth.models import User
from .models import ChatRoom, OnlineUsers
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		
		print("---------------------")
		# print(userlist)
		self.roomGroupName = self.scope['url_route']['kwargs']['roomname']
		self.notificationgroup = "notification"
		await database_sync_to_async(self.user_logged)(self.scope['user'])
		userlist = await database_sync_to_async(self.get_update)()

		print("roomname .......",self.roomGroupName)
		await self.channel_layer.group_add(
			self.roomGroupName ,
			self.channel_name
		)
		print("channel_name",self.channel_name)
		# await self.accept()

		await self.channel_layer.group_add(
			self.notificationgroup ,
			self.channel_name
		)
		print("channel_name",self.channel_name)
		
		await self.accept()
		print("user joined---------------")
	
		# print(updated_user_list)
		await self.channel_layer.group_send(
			self.notificationgroup,{
			"type" : "sendMessage" ,
			"flag": "userstatus",
			"message" : userlist,
			"username" : "username" ,
			}
		)

		
	async def disconnect(self , close_code):
		print("user left---------------")
		await database_sync_to_async(self.user_disconnect)(self.scope['user'])
		userlist = await database_sync_to_async(self.get_update)()
		await self.channel_layer.group_send(
			self.notificationgroup,{
			"type" : "sendMessage" ,
			"flag": "userstatus",
			"message" : userlist,
			"username" : "username" ,
			}
		)
		await database_sync_to_async(self.user_disconnect)(self.scope['user'])
		await self.channel_layer.group_discard(
			self.roomGroupName ,
			self.channel_layer
		)
		await self.channel_layer.group_discard(
			self.notificationgroup ,
			self.channel_layer
		)
		await super().disconnect(close_code)
		

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json["message"]
		username = text_data_json["username"]

		reciver = text_data_json["reciver"]
		reciver = reciver.replace("-","")
		print("-------",reciver)
		user = self.scope.get('user', None)
		reciver = reciver.replace(user.username,"")
		notification_message = f"{reciver} you recived a message from {user.username}"
		print("-------",reciver)
		print(user)

		await self.channel_layer.group_send(
			self.roomGroupName,{
				"type" : "sendMessage" ,
				"flag":"message",
				"message" : message ,
				"username" : username ,
			})
		
		await self.channel_layer.group_send(
			self.notificationgroup,{
				"type" : "sendMessage" ,
				"flag":"notification",
				"message" : notification_message,
				"username" : reciver ,
			})
		await database_sync_to_async(self.update_chat_history)(message,username)
	async def sendMessage(self , event) :
		flag = event["flag"]
		message = event["message"]
		username = event["username"]
		await self.send(text_data = json.dumps({"message":message ,"username":username,"flag":flag}))



	def update_chat_history(self,message,username):
		print(message,username)
		

		message_string_to_update = username +"-"+message
		print("current update",message_string_to_update)
		chat_history_instancne = ChatRoom.objects.get(roomname=self.roomGroupName)
		chat_history_instancne_previous_messages = chat_history_instancne.messages
		print("previous messages",chat_history_instancne_previous_messages)
		if chat_history_instancne_previous_messages =="":
			chat_history_instancne.messages = message_string_to_update
			chat_history_instancne.save()
		else:
			chat_history_instancne.messages = chat_history_instancne_previous_messages + ","+ message_string_to_update
			chat_history_instancne.save()
		print(message_string_to_update)
		return None
	
	def user_logged(self,username):
		all_users = OnlineUsers.objects.get_or_create(user = username)
		all_users[0].status = True
		all_users[0].save()
		return None
	def user_disconnect(self,username):
		all_users = OnlineUsers.objects.get(user = username)
		all_users.status = False
		all_users.save()
		return None
	
	def get_update(self):
		logged_user_instance = OnlineUsers.objects.all()
		print("*"*50)
		logged_user_instance = [{"status": user.status, "name" :user.user.username } for user in logged_user_instance ]
		print(logged_user_instance)

		return logged_user_instance
