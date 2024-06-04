from django.contrib.auth.models import User
from rest_framework import serializers
from authapp.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('address', 'city', 'region', 'zip', 'user_type', 'profile_picture')

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='userprofile')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile')
