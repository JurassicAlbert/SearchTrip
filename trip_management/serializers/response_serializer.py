import pytz
from datetime import datetime
from ..models.response import Response
from rest_framework import serializers


class ResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for Response model.
    """

    class Meta:
        model = Response
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new Response instance.
        """
        return Response.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Response instance.
        """
        instance.response_text = validated_data.get('response_text', instance.response_text)
        instance.date_added = validated_data.get('date_added', instance.date_added)
        instance.save()
        return instance

    def validate_response_text(self, value):
        """
        Validate response_text field to ensure it is not empty.
        """
        if not value.strip():
            raise serializers.ValidationError("Response text cannot be empty.")
        return value

    def validate_date_added(self, value):
        """
        Validate date_added field to ensure it is not in the future.
        """
        if value > datetime.utcnow().replace(tzinfo=pytz.utc):
            raise serializers.ValidationError("Date added cannot be in the future.")
        return value
