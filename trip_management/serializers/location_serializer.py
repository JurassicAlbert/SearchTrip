from rest_framework import serializers
from ..models.location import Location
from .address_serializer import AddressSerializer


class LocationSerializer(serializers.ModelSerializer):
    """
    Serializer for Location model.
    """
    address = AddressSerializer()

    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        """
        Create and return a new Location instance.
        """
        address_data = validated_data.pop('address')
        address_serializer = AddressSerializer(data=address_data)
        address_serializer.is_valid(raise_exception=True)
        address = address_serializer.save()
        return Location.objects.create(address=address, **validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Location instance.
        """
        address_data = validated_data.pop('address', None)
        if address_data:
            address_serializer = AddressSerializer(instance.address, data=address_data)
            address_serializer.is_valid(raise_exception=True)
            address = address_serializer.save()
            validated_data['address'] = address
        instance.location_name = validated_data.get('location_name', instance.location_name)
        instance.description = validated_data.get('description', instance.description)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()
        return instance
