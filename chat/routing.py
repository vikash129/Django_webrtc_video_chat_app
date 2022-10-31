# chat/routing.py
from django.urls import re_path

from . import consumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/(?P<user_name>\w+)/(?P<choice>\w+)$", consumer.ChatConsumer.as_asgi()),
]

# print(websocket_urlpatterns)
# [<URLPattern 'ws/chat'>]

'''  
We need to create a routing configuration for the chat app that has a route to the consumer

We call the as_asgi() classmethod in order to get an ASGI application that will instantiate an instance of our consumer
 for each user-connection. This is similar to Django’s as_view(), which plays the same role for per-request Django view instances.

(Note we use re_path() due to limitations in URLRouter.)


'''