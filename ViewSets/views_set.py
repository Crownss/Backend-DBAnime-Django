from Controllers.serializers import *
from rest_framework.viewsets import ModelViewSet
from Models.models import *


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializers
    # permission_classes = [permissions.IsAuthenticated]

# class FollowViewSet(ModelViewSet):
#     queryset = Follow.objects.all()
#     serializer_class = FollowSerializers
