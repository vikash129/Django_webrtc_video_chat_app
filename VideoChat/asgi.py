import os

# from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VideoChat.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

import chat.routing


from django.core.asgi import get_asgi_application
  

application = ProtocolTypeRouter(
    {
     'http':  get_asgi_application(),
     'websocket': 
        AllowedHostsOriginValidator(
            URLRouter(  chat.routing.websocket_urlpatterns)
            )
    }
)



# print("application", application)

#  <channels.routing.ProtocolTypeRouter object at 0x000001EDAAD35D00>

''' 
The next step is to point the main ASGI configuration at the chat.routing module. 
In mysite/asgi.py, import AuthMiddlewareStack, URLRouter, and chat.routing; and insert a 'websocket' key in the
 ProtocolTypeRouter list in the following format:


This root routing configuration specifies that when a connection is made to the Channels development server, 
the ProtocolTypeRouter will first inspect the type of connection. If it is a WebSocket connection (ws:// or wss://), 
the connection will be given to the AuthMiddlewareStack.

The AuthMiddlewareStack will populate the connection’s scope with a reference to the currently authenticated user, 
similar to how Django’s AuthenticationMiddleware populates the request object of a view function with the currently 
authenticated user. (Scopes will be discussed later in this tutorial.) Then the connection will be given to the URLRouter.

The URLRouter will examine the HTTP path of the connection to route it to a particular consumer, based on the provided url patterns.
'''