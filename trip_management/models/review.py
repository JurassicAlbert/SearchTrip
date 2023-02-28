from .user import User
from django.db import models
from .location import Location


class Review(models.Model):
    """
    Model representing a review.

    Fields:
        user (ForeignKey): The user who wrote the review.
        location (ForeignKey): The location being reviewed.
        review_text (TextField): The text of the review.
        date_added (DateTimeField): The date and time the review was added.
        rating (IntegerField): The rating given to the location by the user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    review_text = models.TextField()
    date_added = models.DateTimeField()
    rating = models.IntegerField()
