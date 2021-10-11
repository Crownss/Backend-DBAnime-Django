from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from Controllers.serializers import FollowSerializers, UsersSerializers
from rest_framework.viewsets import ModelViewSet
from Models.models import *
from rest_framework import permissions


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializers
    # permission_classes = [permissions.IsAuthenticated]

# class FollowViewSet(ModelViewSet):
#     queryset = Follow.objects.all()
#     serializer_class = FollowSerializers
