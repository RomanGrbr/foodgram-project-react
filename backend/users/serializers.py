from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializers, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Follow

User = get_user_model


class CustomUserCreateSerializers(UserCreateSerializers):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'email', 'id', 'password', 'username', 'first_name', 'last_name'
        )


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 
            'last_name', 'is_subscribed'
        )
    
    def get_is_subscribed(self, object):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=object.id).exists()