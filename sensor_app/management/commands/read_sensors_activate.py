from django.core.management.base import BaseCommand
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import time
import random  # To generate dummy data

class Command(BaseCommand):
    help = 'Simulates dummy sensor data and sends it to WebSocket consumers'

    def handle(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        self.stdout.write(self.style.SUCCESS("Simulating sensor data..."))

        try:
            while True:
                # Generate random dummy sensor data
                external_xyz = {
                    "x": round(random.uniform(-10, 10), 2),
                    "y": round(random.uniform(-10, 10), 2),
                    "z": round(random.uniform(-10, 10), 2),
                }
                internal_xyz = {
                    "x": round(random.uniform(-5, 5), 2),
                    "y": round(random.uniform(-5, 5), 2),
                    "z": round(random.uniform(-5, 5), 2),
                }

                # Prepare data to send
                data = {
                    "external": external_xyz,
                    "internal": internal_xyz,
                }

                # Send the data to the 'sensor_data' WebSocket group
                async_to_sync(channel_layer.group_send)(
                    "sensor_data",  # Group name
                    {
                        "type": "send_sensor_data",  # Consumer method to call
                        "data": data,
                    }
                )
                print(f"Broadcasting data to group: {data}")  # Add this log


                self.stdout.write(self.style.SUCCESS(f"Sent data: {data}"))
                time.sleep(1)  # Adjust the frequency of data sending

        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("Stopped simulation"))
