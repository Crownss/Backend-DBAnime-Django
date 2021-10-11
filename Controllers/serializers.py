from Models.models import *
from rest_framework import serializers
from Models.models import User
from django.contrib.auth.hashers import make_password

################# Begin with Serializing data #####################
class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'verif_password',
            'ip_address'
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8
            },
            'verif_password': {
                'write_only': True,
                'min_length': 8
            }
        }
    
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            verif_password=make_password(validated_data['verif_password']),
            ip_address = validated_data['ip_address'],
        )
        if validated_data['password'] != None and validated_data['password'] == validated_data['verif_password']:
            user.save()
            return user

class PostingSerializers(serializers.ModelSerializer):
    class Meta:
        model = PostingModels
        fields = '__all__'
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = CommentModels
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)