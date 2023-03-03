from datetime import datetime
from ..models.user import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        read_only_fields = ['id', 'registration_date']

    def create(self, validated_data):
        """
        Create a new User instance with a hashed password and registration date.
        """
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        validated_data['password'] = hashed_password
        validated_data['registration_date'] = datetime.now()
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing User instance with a hashed password if provided.
        """
        if 'password' in validated_data:
            password = validated_data.pop('password')
            hashed_password = make_password(password)
            instance.password = hashed_password
        return super().update(instance, validated_data)
