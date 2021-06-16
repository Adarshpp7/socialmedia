from channels.generic.websocket import WebsocketConsumer
import json
from .models import *
from asgiref.sync import async_to_sync
from datetime import datetime

#for convert base64 to imagefile
import base64
from django.core.files.base import ContentFile


class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
        
    def disconnect(self,close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        
    def receive(self,text_data):
        data = json.loads(text_data)
        message = data['message']
        msgtype = data['type']
        if msgtype == 'image' or msgtype == 'video' or msgtype == 'audio':
            print('here')
            loop_end = data['loop_end']
        username = data['username']
        receiver = data['receiver']
        full_file = ''
        user1 = User_Profile.objects.get(username=username)
        user2 = User_Profile.objects.get(id=receiver)
        if msgtype == 'image' or msgtype == 'video' or msgtype == 'audio':
            if loop_end == 'true':
                print('last')
                full_file += message
                format, filestr = full_file.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(filestr), name=msgtype + '.' + ext)
                print(data) 
                user_room = Users_Room.objects.get(room_name=self.room_name)
                Messages.objects.create(sender=user1,receiver=user2,users_room=user_room,msg_type=msgtype,upload_file=data)
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'msgtype':msgtype,
                        'message': full_file,
                        'username':username
                        
                    }
                )
            else:
                print('then')
                full_file += message
        else:
            print(user1,user2,datetime.now()) 
            user_room = Users_Room.objects.get(room_name=self.room_name)
            Messages.objects.create(sender=user1,receiver=user2,users_room=user_room, msg_type=msgtype,message=message)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'msgtype':msgtype,
                    'message': message,
                    'username':username
                    
                }
            )
        
    def chat_message(self, event):
        message = event['message']
        msgtype = event['msgtype']
        username = event['username']
        async_to_sync(
            self.send(text_data=json.dumps({
            'message':message,
            'username':username,
            'msgtype':msgtype
            }))
        )  