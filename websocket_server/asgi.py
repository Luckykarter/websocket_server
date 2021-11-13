import os

from django.core.asgi import get_asgi_application
from channels.http import AsgiHandler
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import websocket_server.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websocket_server.settings')
asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
  "http": asgi_app,
  'https': asgi_app,
  'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_server.routing.websocket_urlpatterns
        ))
})