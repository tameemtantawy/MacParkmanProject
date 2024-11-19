import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SensorDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "sensor_data",
            self.channel_name,
        )
        await self.accept()
        print(f"WebSocket connection established: {self.channel_name}")  # Debugging

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "sensor_data",
            self.channel_name,
        )
        print(f"WebSocket disconnected: {self.channel_name}")  # Debugging

    async def send_sensor_data(self, event):
        data = event["data"]
        print(f"Sending data to client: {data}")  # Debugging
        await self.send(text_data=json.dumps(data))
