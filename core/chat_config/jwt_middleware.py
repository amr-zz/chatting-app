from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        token = self.get_token_from_scope(scope)
        user = None
        if token:
            try:
                access_token = AccessToken(token)
                user = await self.get_user(access_token)
            except Exception:
                scope['error'] = 'Invalid token'
        scope['user'] = user or AnonymousUser()
        return await super().__call__(scope, receive, send)

    def get_token_from_scope(self, scope):
        query_string = scope.get('query_string', b'').decode()
        params = dict(x.split('=') for x in query_string.split('&') if '=' in x)
        return params.get('token')

    @database_sync_to_async
    def get_user(self, access_token):
        User = get_user_model()
        try:
            user_id = access_token['user_id']
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None