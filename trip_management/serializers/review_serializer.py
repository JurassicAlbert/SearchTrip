from rest_framework import serializers
from ..models.review import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model.
    """

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['id']

    def validate_rating(self, value):
        """
        Validate that the rating is between 1 and 5.
        """
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_review_text(self, value):
        """
        Validate that the review text is not empty.
        """
        if not value.strip():
            raise serializers.ValidationError("Review text cannot be empty.")
        return value

    def create(self, validated_data):
        """
        Create and return a new Review instance.
        """
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Review instance.
        """
        instance.review_text = validated_data.get('review_text', instance.review_text)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance