
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.http import AsgiHandler

from TunePal.token_auth import TokenAuthMiddlewareStack
import chat.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    # 'websocket': TokenAuthMiddlewareStack(
    #     URLRouter(
    #         chat.routing.websocket_urlpatterns
    #     )
    # ),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
