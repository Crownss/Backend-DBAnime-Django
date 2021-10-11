from django.contrib.auth import login, logout
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from Models.models import *
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from django.db.models import Q


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class RegisterViewSet(ViewSet):
    def post(self, request):
        if request.user.is_authenticated:
            raise AuthenticationFailed('u already logged in !')
        serializer = UsersSerializers(data={'username':request.data['username'], 'email':request.data['email'], 'password':request.data['password'], 'verif_password':request.data['verif_password'], 'ip_address':get_client_ip(request)})
        if serializer.is_valid():
            if request.data['password'] != request.data['verif_password']:
                return Response(
                    {
                        'message':"your password doesn't match"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response(
                {
                    'message' : "Your Account has been created"
                },
                status=status.HTTP_202_ACCEPTED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

class LoginViewSet(ViewSet):
    def post(self, request):
        if request.user.is_authenticated:
            raise AuthenticationFailed('u already logged in !')
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        user_for_update = User.objects.filter(email=email)
        # print(request.META.get("REMOTE_ADDR"))
        if user is None:
            raise AuthenticationFailed('User Not Found!')
        if user.is_active != True:
            raise AuthenticationFailed('Your account is not activated yet, please contact admin for activated your account')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')
        token, created = Token.objects.get_or_create(user=user)
        user_for_update.update(ip_address=get_client_ip(request))
        login(
            request,
            user,
            'rest_framework.authentication.TokenAuthentication',
        )
        response = Response()
        response.data =  {
            'message' : 'success logged in!',
            'id' : user.id,
            'username':user.username,
            'Token' : token.key,
        }
        return response

class LogoutViewSet(ViewSet):
    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            response = Response()
            user.auth_token.delete()
            logout(request)
            response.delete_cookie('Bearer')
            response.delete_cookie('sessionid')
            response.delete_cookie('Token')
            response.data = {
                'message' : 'success logged out!'
            }
            return response
        raise AuthenticationFailed('Cannot logged out, even u not logged in !')

class PostingViewSet(ViewSet):
    def get(self, request):
        pass
    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
    def update(self, request):
        if request.user.is_authenticated:
            user = request.user
    def delete(self, request):
        if request.user.is_authenticated:
            user = request.user

class CommentViewSet(ViewSet):
    def get(self, request):
        pass
    def post(self, request):
        pass
    def update(self, request):
        pass
    def delete(self, request):
        pass