import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from r_chat import routing  # Ensure this is correct

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wechat.settings')

try:
    django_asgi_app = get_asgi_application()
except Exception as e:
    print("Error initializing Django ASGI application:", e)

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
