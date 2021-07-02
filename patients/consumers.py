import json
from channels.generic.websocket import AsyncWebsocketConsumer


class VideoCallSignalConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('Signal connect')
        self.roomCode = self.scope['url_route']['kwargs']['roomCode']
        self.room_group_name = 'videoCall_%s' % self.roomCode
        # join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print('Signal disconnect')
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(' Signal receive')
        received_data = json.loads(text_data)
        message = received_data['message']
        action = received_data['action']
        print(action)

        if(action == 'new-offer') or (action == 'new-answer'):
            receiver_channel_name = received_data['message']['receiver_channel_name']
            received_data['message']['receiver_channel_name'] = self.channel_name

            await self.channel_layer.send(
                receiver_channel_name,
                {
                    'type': 'signal_sdp',
                    'data': received_data,
                    'message': message,
                    'sender_channel_name': self.channel_name
                }
            )

            return

        received_data['message']['receiver_channel_name'] = self.channel_name

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'signal_sdp',
                'data': received_data,
                'message': message,
                'sender_channel_name': self.channel_name
            }
        )

    async def signal_sdp(self, event):
        data = event['data']

        # Send message to all channels except parent channel
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps(data))