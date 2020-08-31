from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from iot.api.serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny

# helpful link
# https://medium.com/@yerkebulan199/django-rest-framework-drf-token-authentication-with-expires-in-a05c1d2b7e05


@api_view(['POST', ])
#  @authentication_classes([TokenAuthentication])
#  @permission_classes([IsAuthenticated])
def get_emails(request):
    emails = User.objects.values_list('email', flat=True)
    return Response(data={'emails': emails})


@api_view(['POST', ])
@permission_classes([AllowAny])
def api_login(request):
    p = request.POST.copy()
    if p.get('email'):
        username = User.objects.get(email=p['email']).username
        p['username'] = username
    user = authenticate(username=p['username'], password=p['password'])
    res = 'Incorrect'
    token = 'null'
    date = 'null'
    if user is not None:
        #  login(request, user)
        res = 'Correct'
        try:
            token_obj = Token.objects.get(user_id=user.id)
            token = token_obj.key
            date = token_obj.created
        except Token.DoesNotExist:
            token_obj = Token.objects.create(user=user)
            token = token_obj.key
            date = token_obj.created
    data = {
        'api_login': 'You are trying to login',
        'response': res,
        'token': token,
        'date': date
    }
    return Response(data=data)


@api_view(['POST', ])
@permission_classes([AllowAny])
def api_signup(request):
    p = request.POST.copy()
    user = User.objects.create_user(
        username=p['username'].lower(),
        password=p['password'],
        email=p['email']
    )
    token_obj = Token.objects.create(user=user)
    token = token_obj.key
    date = token_obj.created
    data = {
        'api_login': 'You are trying to signup',
        'token': token,
        'date': date
    }
    return Response(data=data)
