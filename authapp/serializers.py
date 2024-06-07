# serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        profile = UserProfile.objects.filter(user__id=obj.id).first()
        if profile:
            return profile.user_type
        return None
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'type')


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    address = serializers.CharField()
    city = serializers.CharField()
    region = serializers.CharField()
    zip = serializers.CharField()
    user_type = serializers.CharField()
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'address', 'city', 'region', 'zip', 'user_type', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        address = validated_data.pop('address')
        city = validated_data.pop('city')
        region = validated_data.pop('region')
        zip = validated_data.pop('zip')
        user_type = validated_data.pop('user_type')
        profile_picture = validated_data.pop('profile_picture', None)

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        UserProfile.objects.create(
            user=user,
            address=address,
            city=city,
            region=region,
            zip=zip,
            user_type=user_type,
            profile_picture=profile_picture
        )
        return user
