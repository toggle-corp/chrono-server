from django.contrib.auth import get_user_model, authenticate
from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Profile

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'username',
            'password',
        )

    def validate_username_email(self, username, email):
        if User.object.filter(username=username, email=email).exists():
            raise ValidationError("Credentials already in use")
    
    def save(self, *kwargs):
        return User.objects.create(
            first_name=self.validated_data.get('first_name',''),
            last_name=self.validated_data.get('last_name',''),
            username=self.validated_data.get('username',''),
            email=self.validated_data['email'],
            password=self.validated_data['password'],
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('eamil','')
        password = attrs.get('password','')
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError('Invalid Credentials')
        attrs.update(dict(user=user))
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = '__all__'
        