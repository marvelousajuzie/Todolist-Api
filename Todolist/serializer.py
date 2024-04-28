from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, TodoList


class CustomUserRegisterserializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    password2 = serializers.CharField(write_only = True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'password2']

    def validate_email(self, value):
        if CustomUser.objects.filter(email= value).exists():
            raise serializers.ValidationError('Email Already In Use')
        return value
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Password Do Not Match')
        return data
    

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(
            email = validated_data['email'],
            username = validated_data['username'],
            password = validated_data.get('password'),
            
        )
        return user



class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(max_length= 150, write_only = True)

    class Meta:
        model = CustomUser
        fields = ['email','password']


        



class Todolistserializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields =  ['title', 'description', 'user']









