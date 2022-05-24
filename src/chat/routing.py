from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
    re_path(r'ws/chat/@me/(?P<dest_id>\w+)/$', consumers.PrivateChatRoomConsumer.as_asgi())
]