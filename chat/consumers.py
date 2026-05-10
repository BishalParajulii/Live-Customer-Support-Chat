import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatSession, ChatMessage



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.group_name = f'chat_{self.session_id}'
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        
        await self.set_session_active()
        
        
        
    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        msg_type = data.get('type')
        
        if msg_type == 'message':
            content = data.get('content' , '').strip()
            sender_type = data.get('sender_type' , 'customer')
            
            if content:
                await self.save_message(sender_type, content)
                
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'chat_message',
                        'sender_type': sender_type,
                        'content': content,
                    }
                )
        elif msg_type == 'typing':
            sender_type = data.get('sender_type' , 'customer')
            
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'typing_indicator',
                    'sender_type': sender_type,
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'sender_type': event['sender_type'],
            'content': event['content'],
        }))
        
    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'sender_type': event['sender_type'],
        }))
        
    @database_sync_to_async
    def save_message(self, sender_type, content):
        session = ChatSession.objects.get(id=self.session_id)
        message = ChatMessage.objects.create(
            session=session,
            sender=sender_type,
            content=content
        )
        return message
    
    @database_sync_to_async
    def set_session_active(self):
        ChatSession.objects.filter(id=self.session_id).update(status='active')
            
            
        
