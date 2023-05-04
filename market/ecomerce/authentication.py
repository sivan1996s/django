from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header,BaseAuthentication
from rest_framework.permissions import BasePermission
import jwt
import json
import locale
import logging
from ecomerce.models import Account
from ecomerce.resolver import decrypt_token_data


logger = logging.getLogger(__name__)


class JWTAuthentication(BaseAuthentication):
    def get_model(self):
        return Account
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            return None
        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header'
            raise exceptions.AuthenticationFailed(msg)
        try:
            token = auth[1]
            if token == "null":
                msg = 'Null token not allowed'
                raise exceptions.AuthenticationFailed(msg)
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)
        channel = request.META.get('HTTP_X_CHANNEL')
        if channel:
            channel = json.loads(channel)
            logger.info('Channel {}'.format(channel))
            if channel.get('user_role'):
                request.user_role = channel.get('user_role')
        user, token, ident = self.authenticate_credentials(token)
        if ident.get('user_id'):
            request.user_id  = ident.get('user_id')
        else:
            return (None)

        return (user, token,)

    def authenticate_credentials(self, token):
        model = self.get_model()
        try:
            public_key = open('public_key.txt').read()
            load = jwt.decode(token, public_key,  'RS256')                                                             
            pay_data = load.get('data')
            if not pay_data:
                logger.info('Token has no data')  
                raise exceptions.AuthenticationFailed('Invalid Token')
            tokens = json.loads(decrypt_token_data(pay_data))
            print('token_data',)
            user_id = tokens.get('user_id')
            user = model.objects.get(id=user_id, is_active=True)
            
        
            if tokens.get('user_id'):
                user_id = tokens.get('user_id')
                return (user, token, {'user_id': user_id})
            else:
                return (None, None, None)

        except Account.DoesNotExist as le:
            logger.exception('Exception {}'.format(le.args))
            raise exceptions.AuthenticationFailed('You are not authorized')

        except jwt.ExpiredSignature as se:
            logger.exception('Exception {}'.format(se.args))
            raise exceptions.AuthenticationFailed('Token is expired')

        except jwt.DecodeError or jwt.InvalidTokenError:
            logger.exception('JWT Error')
            raise exceptions.AuthenticationFailed('Invalid Token')

    def authenticate_header(self, request):
        return 'Token'

class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user:
            if not isinstance(request.user, AnonymousUser):
                return True
        return False
class WebsocketTokenAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        logger.info('Inside WebsocketTokenAuthMiddleware')
        headers = dict(scope['headers'])
        logger.info('Headers {}'.format(headers))
        close_old_connections()
        if b'authorization' in headers:
            logger.info('Inside if')
            try:
                token_name, token_key = headers[b'authorization'].decode().split()
                if token_name == 'Token':
                    public_key = open('public_key.txt').read()
                    payload = jwt.decode(token_key, public_key, 'RS256')
                    payload_data = payload.get('data')
                    if not payload_data:
                        logger.info('Token has no data in Websocket')
                        return None

                    token_data = json.loads(decrypt_token_data(payload_data))
                    user_id = token_data.get('user_id')
                    user = Account.objects.get(id=user_id)
                    if token_data.get('doctor_id'):
                        user_id = token_data.get('user_id')
                        scope['user'] = user
                        scope['user_id'] = user_id
                        return self.inner(scope)
                return None
            except Account.DoesNotExist:
                return None
            except Exception as e:
                logger.exception('Exception {}'.format(e.args))
                return None
        return None

WebsocketTokenAuthMiddlewareStack = lambda inner: WebsocketTokenAuthMiddleware(AuthMiddlewareStack(inner))