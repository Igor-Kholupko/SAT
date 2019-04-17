from django.urls import path

from chat import consumers

websocket_urlpatterns = [
    path('ws/chat/<username>/', consumers.ChatConsumer),
    path('ws/notificator/', consumers.NotificatorConsumer),
]
