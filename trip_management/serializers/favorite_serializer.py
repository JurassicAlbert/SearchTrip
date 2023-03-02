from ..models.favorite import Favorite
from rest_framework import serializers
from .user_serializer import UserSerializer
from .location_serializer import LocationSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Serializer for Favorite model.
    """
    user = UserSerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new Favorite instance.
        """
        return Favorite.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Favorite instance.
        """
        instance.user = validated_data.get('user', instance.user)
        instance.location = validated_data.get('location', instance.location)
        instance.save()
        return instance

    def validate(self, attrs):
        """
        Check that user and location are not null and that the user has not already favorited the location.
        """
        user = attrs.get('user')
        location = attrs.get('location')
        if not user:
            raise serializers.ValidationError("User must be provided.")
        if not location:
            raise serializers.ValidationError("Location must be provided.")
        if Favorite.objects.filter(user=user, location=location).exists():
            raise serializers.ValidationError("User has already favorited this location.")
        return attrs
