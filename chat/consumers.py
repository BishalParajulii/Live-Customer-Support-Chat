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
        
        history = await self.get_history()
        
        for message in history:
            await self.send(text_data=json.dumps({
                'type': 'message',
                'sender_type': message['sender_type'],
                'content': message['content'],
                'timestamp': message['timestamp'],
                'is_read': message['is_read'],
            }))
            
        
        
        
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
                message = await self.save_message(sender_type, content)
                
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'chat_message',
                        'sender_type': sender_type,
                        'content': content,
                        'timestamp': message['timestamp'],
                        'is_read': False,
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
        elif msg_type == 'read':
            reader_type = data.get('sender_type', 'customer')
            await self.mark_messages_read(reader_type)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'read_receipt',
                    'reader_type': reader_type,
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'sender_type': event['sender_type'],
            'content': event['content'],
            'timestamp': event.get('timestamp', ''),
            'is_read': event.get('is_read', False),
        }))
        
    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'sender_type': event['sender_type'],
        }))
        
    async def read_receipt(self, event):
        await self.send(text_data=json.dumps({
            'type': 'read',
            'reader_type': event['reader_type'],
        }))
       
    @database_sync_to_async 
    def get_history(self):
        messages = ChatMessage.objects.filter(session_id=self.session_id).order_by('timestamp')[:50]
        return [{
            'content' : m.content,
            'sender_type' : m.sender,
            'timestamp' : m.timestamp.strftime('%H:%M'),
            'is_read': m.is_read,
        } for m in messages
        ]
        

    @database_sync_to_async
    def save_message(self, sender_type, content):
        session = ChatSession.objects.get(id=self.session_id)
        message = ChatMessage.objects.create(
            session=session,
            sender=sender_type,
            content=content
        )
        return {
            'id': message.id,
            'timestamp': message.timestamp.strftime('%H:%M'),
        }
    
    @database_sync_to_async
    def set_session_active(self):
        ChatSession.objects.filter(id=self.session_id).update(status='active')
        
    @database_sync_to_async
    def mark_messages_read(self, reader_type):
        ChatMessage.objects.filter(
            session_id=self.session_id,
            is_read=False,
        ).exclude(sender=reader_type).update(is_read=True)
            
            
        
