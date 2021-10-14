from django.contrib.auth import login, logout
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from Models.models import *
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, NotFound, PermissionDenied, ValidationError
from rest_framework.authtoken.models import Token
from django.db.models import Q
from Helpers import get_client_ip
########################################################################################################

class RegisterViewSet(ViewSet):

    def post(self, request):
        if request.user.is_authenticated:
            raise AuthenticationFailed('u already logged in !')
        serializer = UsersSerializers(data={'username':request.data['username'], 'email':request.data['email'], 'password':request.data['password'], 'verif_password':request.data['verif_password'], 'ip_address':get_client_ip(request)})
        if serializer.is_valid():
            if request.data['password'] != request.data['verif_password']:
                raise ValidationError("password does'nt match !")
            serializer.save()
            return Response(
                {
                    'message' : "Your Account has been created"
                },
                status=status.HTTP_202_ACCEPTED
            )
        raise ValidationError

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
        query = request.GET.get('postid')
        if query:
            posting_models = PostingModels.objects.filter(id=query)
            if posting_models != None | 0:
                return Response({'data':posting_models.values()},status=status.HTTP_200_OK)
            raise NotFound
        posting_models = PostingModels.objects.all()
        return Response({'count':posting_models.count(), 'data':posting_models.values()},status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            admin_check = User.objects.filter(username=user.username).first()
            if admin_check.is_superuser != True:
                raise PermissionDenied
            posting_serializers = PostingSerializers(data={'author':request.username, 'img':request.data['img'], 'title':request.data['title'], 'desc':request.data['desc'], 'description':request.data['description']})
            if posting_serializers.is_valid():
                posting_serializers.save()
                return Response({'message':'posted !'},status=status.HTTP_201_CREATED)
            raise ValidationError
        raise NotAuthenticated('loggin first !')

    def update(self, request):
        if request.user.is_authenticated:
            user = request.user
            query = request.GET.get('postid')
            if query:
                admin_check = User.objects.filter(username=user.username).first()
                if admin_check.is_superuser != True:
                    raise PermissionDenied
                posting_models = PostingModels.objects.filter(id=query)
                posting_serializers = PostingSerializers
                if posting_models.count() != 0:
                    posting_serializers.update(self, instance=posting_models, validated_data={'author':user.username, 'img':request.data['img'], 'title':request.data['title'], 'desc':request.data['desc'], 'description':request.data['description'], 'link':request.data['link']})
                raise NotFound
        raise NotAuthenticated('loggin first !')

    def delete(self, request):
        if request.user.is_authenticated:
            user = request.user
            admin_check = User.objects.filter(username=user.username).first()
            if admin_check.is_superuser != True:
                raise PermissionDenied
            query = request.GET.get('postid')
            if query:
                posting_models = PostingModels.objects.filter(id=query)
                if posting_models != None & 0:
                    return Response({'data':posting_models.values().first()},status=status.HTTP_200_OK)
                raise NotFound('not found any data with id: '+ query)
        raise NotAuthenticated('loggin first !')


class CommentViewSet(ViewSet):

    def get(self, request):
        query = request.GET.get('postid')
        if query:
            comment_models = CommentModels.objects.filter(toPost=query)
            if comment_models.count != 0:
                return Response({'count':comment_models.count(), 'data':comment_models.values(), 'message':'found !'},status=status.HTTP_302_FOUND)
            raise NotFound
        comment_models = CommentModels.objects.all()
        return Response({'count':comment_models.count(), 'data':comment_models.values(),'message':'found all commentar !'},status=status.HTTP_200_OK)
    
    def post(self, request):
        query = request.GET.get('postid')
        if query:
            posting_models = PostingModels.objects.get(id=query)
            comment_serializers = CommentSerializers(data={'username':request.data['username'], 'comment':request.data['comment'], 'toPost':posting_models, 'ip_address':get_client_ip(request)})
            if comment_serializers.is_valid():
                comment_serializers.save()
                return Response({'message':'success comment !'},status=status.HTTP_201_CREATED)
            raise ValidationError
        # comment_serializers = CommentSerializers(data={'username':request.data['username'], 'comment':request.data['comment'], 'toPost':None, 'ip_address':get_client_ip(request)})
        # if comment_serializers.is_valid():
        #     comment_serializers.save()
        #     return Response({'message':'success comment !'},status=status.HTTP_202_ACCEPTED)
        # return Response({'message':'something wrong with your request !'},status=status.HTTP_400_BAD_REQUEST)

    def update(self, request):
        query = request.GET.get('postid')
        if query:
            comment_models = CommentModels.objects.filter(toPost=query, ip_address=get_client_ip(request))
            comment_serializers = CommentSerializers
            if comment_models.count() != 0:
                comment_serializers.update(self, instance=get_client_ip(request), validated_data={'username':request.data['username'], 'comment':request.data['comment'], 'toPost':comment_models, 'ip_address':get_client_ip(request)})
                return Response({'message':'updated your comment !'},status=status.HTTP_202_ACCEPTED)
            raise NotFound
        raise NotFound

    def delete(self, request):
        query = request.GET.get('postid')
        if query:
            comment_models = CommentModels.objects.filter(toPost=query, ip_address=get_client_ip(request))
            if comment_models.count() != 0:
                comment_models.delete()
                return Response({'message':'deleted !'})
            raise NotFound
        raise NotFound