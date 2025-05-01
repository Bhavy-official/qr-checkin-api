from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'studentID', 'full_name', 'password', 'role']  
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    studentID = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        studentID = data.get("studentID")
        password = data.get("password")

        user = authenticate(request=self.context.get('request'), studentID=studentID, password=password)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")

