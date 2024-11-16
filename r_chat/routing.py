from django.urls import path , include,re_path
from r_chat.consumers import ChatConsumer

# WebSocket URL routing
websocket_urlpatterns = [
    # re_path(r'^ws/(?P<room_slug>[^/]+)/$', ChatConsumer.as_asgi()),
    path("<room_slug>" , ChatConsumer.as_asgi()) ,
    # re_path(r'^ws/(?P<room_slug>[^/]+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/(?P<room_slug>[^/]+)/$', ChatConsumer.as_asgi()),
    
]