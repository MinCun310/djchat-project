from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import JsonWebsocketConsumer

from asgiref.sync import async_to_sync

class MyConsumer(JsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = 'testserver'

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)

    def receive_json(self, content):
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                "type": "chat.message",
                "new_message": content['message'],
            },
        )

    def chat_message(self, event):
        async_to_sync(self.send_json(event))

    def disconnect(self, close_code):
        pass