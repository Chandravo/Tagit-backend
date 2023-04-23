from django.urls import re_path,path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
    # path('ws/chat/dd/', consumers.ChatRoomConsumer.as_asgi()),
    # re_path(r'ws/chat/aa/', consumers.ChatRoomConsumer),
]