import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ScanConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.scan_id = self.scope['url_route']['kwargs']['scan_id']
        self.group_name = f'scan_{self.scan_id}'

        # Simple verification: Check if scan exists in DB
        # Note: In a real prod env, we'd use sync_to_async to query
        from asgiref.sync import sync_to_async
        from apps.scans.models import Scan
        
        @sync_to_async
        def scan_exists(sid):
            return Scan.objects.filter(id=sid).exists()
            
        if not await scan_exists(self.scan_id):
            await self.close()
            return

        # Join scan group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave scan group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from room group
    async def scan_update(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'update',
            'data': message
        }))
