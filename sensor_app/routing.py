from django.urls import path
from .consumers import SensorDataConsumer  # Import your WebSocket consumer

websocket_urlpatterns = [
    path('ws/sensor-data/', SensorDataConsumer.as_asgi()),
]

