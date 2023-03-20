from ..models.address import Address
from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for Address model.
    """
    latitude = serializers.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = serializers.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    postal_code = serializers.CharField(validators=[RegexValidator(r'^\d{2}-\d{3}$')])

    class Meta:
        model = Address
        fields = ['id', 'street_name', 'street_number', 'city', 'state_province', 'postal_code', 'latitude',
                  'longitude']
        read_only_fields = ['id']

    def create(self, validated_data):
        """
        Create and return a new Address instance.
        """
        return Address.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Address instance.
        """
        instance.street_name = validated_data.get('street_name', instance.street_name)
        instance.street_number = validated_data.get('street_number', instance.street_number)
        instance.city = validated_data.get('city', instance.city)
        instance.state_province = validated_data.get('state_province', instance.state_province)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.save()
        return instance
