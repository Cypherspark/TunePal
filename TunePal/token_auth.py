from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope):
        headers = dict(scope['headers'])
        if b'cookie' in headers:
            try:
                token_name = headers[b'cookie'].decode().split()[2]
                token_key = headers[b'cookie'].decode().split()[3]
                if token_name == 'Authorization:Token':
                    token = await database_sync_to_async(Token.objects.get(key=token_key))()
                    scope['user'] = token.user
            except Token.DoesNotExist:
                scope['user'] = AnonymousUser()
        return self.inner(scope)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))