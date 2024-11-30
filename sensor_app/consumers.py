# consumers.py
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .read_sensors import LogicHandler  # Import the LogicHandler to access your sensor data

# Instantiate the LogicHandler to access sensor data
logic_handler = LogicHandler()

class SensorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "sensor_data"  # Room group name for broadcasting to clients

        # Join WebSocket group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Start sending data to the WebSocket periodically
        self.data_sender_task = asyncio.create_task(self.send_data_periodically())

    async def disconnect(self, close_code):
        # Leave WebSocket group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Cancel the task to stop sending data
        self.data_sender_task.cancel()

    async def send_data_periodically(self):
        """Periodically send data every second (or as needed)"""
        while True:
            # Fetch sensor data
            external_xyz, internal_xyz = logic_handler.read_xyz_data()

            # Send data over WebSocket
            await self.send(text_data=json.dumps({
                'external': external_xyz,
                'internal': internal_xyz
            }))
            
            # Wait for the next interval (e.g., 1 second)
            await asyncio.sleep(0.1)
